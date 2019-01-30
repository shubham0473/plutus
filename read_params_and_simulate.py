#! /usr/bin/env python
import io, sys, os
from os import listdir
from os.path import isfile, join
import pandas as pd
import model

MAX_POS     = 1
SLIPPAGE    = 0.75

def getDate(datafile_):
    if (os.path.getsize(datafile_)):
        with open(datafile_) as f:
            first_line_ = f.readline()
            if first_line_:
                line_ = first_line_.rstrip().split()
                if (len(line_)  <= 7):
                    print "Data corrupt for " + datafile_
                    exit()
                else:
                    return line_[0]


def simulateForADay(my_model_, datafile_):
    if os.path.isfile(datafile_):
        thisdate_ = getDate(datafile_)
        with open(datafile_) as f:
            lines_ = f.readlines()
            current_pos_    = 0
            volume_traded_  = 0
            current_pnl_    = 0
            min_pnl_        = 0
            invested_amt_   = 0

            for line_ in lines_:
                line_ = line_.rstrip().split()
                time_ = line_[1]
                bid_px_ = float(line_[2])
                ask_px_ = float(line_[3])
                indicatorlist_ = map(float, line_[5:])
                signal_ = my_model_.getSignal(indicatorlist_)
		print signal_
                target_price_ = signal_ + (bid_px_ + ask_px_)/2.00
                if (time_ >= "03:50:00" and time_ <= "09:50:00" ):
                    #Signal activated for buy
                    if(target_price_ - bid_px_ >= my_model_.threshold_[0]):
                        if(current_pos_ < MAX_POS):
                            current_pos_ += 1
                            volume_traded_ += 1
                            fill_price_ = (1 + SLIPPAGE/10000.0) * (bid_px_ + ask_px_)/2.00
                            invested_amt_ += fill_price_

                    #Signal activated for sell
                    if(target_price_ - ask_px_ <=  -1 * my_model_.threshold_[0]):
                        if(current_pos_ > -1 * MAX_POS):
                            current_pos_ -= 1
                            volume_traded_ += 1
                            fill_price_ = (1 - SLIPPAGE/10000.0) * (bid_px_ + ask_px_)/2.00
                            invested_amt_ -= fill_price_

                    
                else:
                    #Exchange is about to close, square off all positions
                    if (current_pos_ > 0):
                        current_pos_ -= 1
                        volume_traded_ += 1
                        fill_price_ = (1 - SLIPPAGE/10000.0) * (bid_px_ + ask_px_)/2.00
                        invested_amt_ -= fill_price_

                    elif(current_pos_ < 0):
                        current_pos_ += 1
                        volume_traded_ += 1
                        fill_price_ = (1 + SLIPPAGE/10000.0) * (bid_px_ + ask_px_)/2.00
                        invested_amt_ += fill_price_
            
                current_pnl_ = (current_pos_ * (bid_px_ + ask_px_)/2.00 - invested_amt_)
                if(current_pnl_ < min_pnl_):
                    min_pnl_ = current_pnl_
            return [thisdate_, current_pnl_, min_pnl_, volume_traded_, current_pos_]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: ./read_params_and_simulate.py paramfile datalocation" 
        exit()

    paramfile_      = sys.argv[1]
    datalocation_   = sys.argv[2]
   
    #Make an object of model class
    my_model_ = model.Model(paramfile_)

    #Parse through the data folder and list all files
    onlyfiles_ = [f for f in listdir(datalocation_) if isfile(join(datalocation_, f))]
    
    #Run simulations on all days
    stats_mat_ = []
    for file_ in onlyfiles_:
        thisdayfile_ = datalocation_ + "/" + file_
        thisday_stats_ =  simulateForADay(my_model_, thisdayfile_)
        stats_mat_.append(thisday_stats_)

    #Obtain and print the statistics
    df_ = pd.DataFrame(stats_mat_, columns=['Date', 'PNL', 'MINPNL', 'TRADES', 'EODPOS'])
    pd.set_option('display.max_colwidth', -1)
    print (df_.to_string(index=False) + "\n")
    print "STATS   AvgPNL: " + str(df_['PNL'].mean()) + "  Sharpe: " + str(df_['PNL'].mean() / df_['PNL'].std()) + "  AvgTrades: " + str(df_['TRADES'].mean())

