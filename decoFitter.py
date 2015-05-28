#!/usr/bin/env python
################################################################################
# Going to take a histagram as input and run a fit for different ranges
################################################################################

import os
from ROOT import gROOT, gStyle
import ROOT
from array import array
import argparse

p = argparse.ArgumentParser(description="Target image path file (sans .txt): HTC_A510, SPH-D710VMUB, RAZR, SAMSUNG-SGH, standard")
p.add_argument("file", nargs=1,
                       help="target image path file")
args = p.parse_args()
filename = args.file[0]

ifile = ROOT.TFile("%s" % filename, "r")
if 'HTC' in filename:
    histName = "HTC Wildfire Slength"
if 'SPH' in filename:
    histName = "Samsung Galaxy S2length"
hist = ifile.Get(histName)

binWidth = int( hist.GetBinWidth(1) )
print "Bin width: %i" % binWidth
nBins = hist.GetXaxis().GetNbins()
print "Number of bins: %i" % nBins
Max = nBins * binWidth
print "X range: 0 - %i" % Max

xMin = []
for i in range(1, 4):
    xMin.append(i * binWidth)
xMax = []
for i in range(4, 12):
    xMax.append(i * binWidth)
print xMin
print xMax
#xMax = [90, 100]

''' Do some fitting to find the depth of the depletion region '''
storage = []
for mini in xMin:
    for maxi in xMax:
        print "x range: %i-%i" % (mini, maxi)
        #funx = ROOT.TF1( 'funx', '[0] * cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', (nMax/nBins)*fitMin, nMax)
        funx = ROOT.TF1( 'funx', '[0]*cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', mini, maxi)
        #$  funx = ROOT.TF1( 'funx', '(1/(1+TMath::Exp([2]*(x-[3]))))*[0] * cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', 0, nMax)
        f1 = gROOT.GetFunction('funx')
        f1.SetParName( 0, "vert count" )
        f1.SetParName( 1, "depth" )
        f1.SetParameter( 0, 999 )
        f1.SetParameter( 1, 999 )
        #$  f1.SetParName( 2, "steepness" )
        #$  f1.SetParameter( 2, -1 )
        #$  f1.SetParName( 3, "x offset" )
        #$  f1.SetParameter( 3, 3 )
          
        rslt = hist.Fit('funx', 'EMRISW')
        fitResult = hist.GetFunction("funx")
        fitVert = round(fitResult.GetParameter( 0 ), 0)
        fitDepth = round(fitResult.GetParameter( 1 ), 3)
        fitVertError = round(fitResult.GetParError( 0 ), 0)
        fitDepthError = round(fitResult.GetParError( 1 ), 3)
        #$  fitSteep = fitResult.GetParameter( 2 )
        #$  fitOffset = fitResult.GetParameter( 3 )
        #$  fitSteepError = fitResult.GetParError( 2 )
        #$  fitOffsetError = fitResult.GetParError( 3 )
        accurate = rslt.IsValid()
        storage.append( [mini, maxi, fitVert, fitVertError, fitDepth, fitDepthError, accurate] )
        

#print storage
for line in storage:
    print "x range: %3i-%3i  vert: %8i+-%8i  depth: %10f+-%10f   accurate: %7s" % (line[0], line[1], line[2], line[3], line[4], line[5], line[6])

gROOT.cd()



