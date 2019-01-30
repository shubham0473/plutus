#! /usr/bin/env python

class Model:
    def __init__(self, paramfile_):
        threshold_, weights_array_ = self.readParamFile(paramfile_)
        self.weights_ = weights_array_
        self.threshold_ = threshold_
    
    #Reading the param file
    def readParamFile(self, paramfile_):
        weights_array_ = []
        threshold_ = []
        with open(paramfile_) as f:
            lines_ = f.readlines()
            for line_ in lines_:
                line_ = line_.rstrip()
                if(line_):
                    linesplit_  = line_.split(":")
                    header_     = linesplit_[0].strip()
                    value_      = linesplit_[1].strip().replace(" ", "").split(",")
                    if (header_ == "WEIGHTS"):
                        value_ = map(float, value_)
                        weights_array_ = value_
                    if (header_ == "THRESHOLD"):
                        threshold_ = [float(value_[0])]
                    #print header_, value_
        if( not weights_array_ or not threshold_):
            print "Incorrect param file!. Make sure it is in desired format"
            exit()
        else:
            return threshold_, weights_array_

    #Get signal, this is a simple linear aggregator. One may replace this by complex one
    def getSignal(self, indicatorlist_):
        if (len(indicatorlist_) != len(self.weights_)) :
            print "Weight list is not correct required " + str(len(indicatorlist_)) + " weights, got " + str(len(self.weights_))
            exit()
        return sum([x*y for x,y in zip(indicatorlist_, self.weights_)])

