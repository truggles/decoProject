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

#fitCode = 'EMRISWW'
#fitCode = 'EMRISW'
fitCode = 'EMRIS'
#isotropic = False
isotropic = True

#for fitCode in ['EMRISWW', 'EMRISW', 'EMRIS']:
ifile = ROOT.TFile("%s" % filename, "r")
if '2010' in filename:
    num = '2010'
if '405' in filename:
    num = '405'
if '8025' in filename:
    num = '8025'
if 'HTC' in filename:
    histName = "HTC Wildfire Slength"
    saveName = "HTC_Wildfire_S"
    titleName = "HTC Wildfire S"
    abrev = 'HTC'
if 'SPH' in filename:
    histName = "Samsung Galaxy S2length"
    saveName = "Samsung_Galaxy_S2"
    titleName = "Samsung Galaxy S2"
    abrev = 'SPH'
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
for i in range(4, 11):
    xMax.append(i * binWidth)
xMin = [binWidth]
#xMax = [90, 100]
print xMin
print xMax

''' Do some fitting to find the depth of the depletion region '''
''' I previously forgot the dl / dTheta, that is the new 1/(1+x^2) component '''
storage = []
folder = 'fits%s%s' % (abrev, num)
if isotropic: folder = folder + 'iso'
for mini in xMin:
    for maxi in xMax:
        print "x range: %i-%i" % (mini, maxi)
        #funx = ROOT.TF1( 'funx', '[0] * cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', (nMax/nBins)*fitMin, nMax)
        #funx = ROOT.TF1( 'funx', '[0]*cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', mini, maxi)
        #funx = ROOT.TF1( 'funx', '[0]*cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )*( 1 / ([1]*( 1 + ((x*x)/([1]*[1])))))', mini, maxi)
        #if isotropic: funx = ROOT.TF1( 'funx', '[0]*sin( TMath::ATan( x / [1]) )*( 1 / ([1]*( 1 + ((x*x)/([1]*[1])))))', mini, maxi)
        funx = ROOT.TF1( 'funx', '([0] * x * [1]*[1]*[1]*[1])/( (x*x+[1]*[1])*(x*x+[1]*[1])*(x*x+[1]*[1]) )', mini, maxi)
        if isotropic: funx = ROOT.TF1( 'funx', '([0] * x * [1]*[1])/( (x*x+[1]*[1])*(x*x+[1]*[1]) )', mini, maxi)
        #$  funx = ROOT.TF1( 'funx', '(1/(1+TMath::Exp([2]*(x-[3]))))*[0] * cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', 0, nMax)
        f1 = gROOT.GetFunction('funx')
        f1.SetParName( 0, "scale" )
        f1.SetParName( 1, "depth" )
        f1.SetParameter( 0, 999 )
        f1.SetParameter( 1, 999 )
        #$  f1.SetParName( 2, "steepness" )
        #$  f1.SetParameter( 2, -1 )
        #$  f1.SetParName( 3, "x offset" )
        #$  f1.SetParameter( 3, 3 )
          
        rslt = hist.Fit('funx', fitCode)
        fitResult = hist.GetFunction("funx")
        fitScale = round(fitResult.GetParameter( 0 ), 0)
        fitDepth = round(fitResult.GetParameter( 1 ), 3)
        fitScaleError = round(fitResult.GetParError( 0 ), 0)
        fitDepthError = round(fitResult.GetParError( 1 ), 3)
        #$  fitSteep = fitResult.GetParameter( 2 )
        #$  fitOffset = fitResult.GetParameter( 3 )
        #$  fitSteepError = fitResult.GetParError( 2 )
        #$  fitOffsetError = fitResult.GetParError( 3 )
        accurate = rslt.IsValid()

        ''' save histos with fit '''
        #funNew = ROOT.TF1( 'funNew', '[0]*cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )*( 1 / ([1]*( 1 + ((x*x)/([1]*[1])))))', 0, Max)
        #if isotropic: funNew = ROOT.TF1( 'funNew', '[0]*sin( TMath::ATan( x / [1]) )*( 1 / ([1]*( 1 + ((x*x)/([1]*[1])))))', 0, Max)
        funNew = ROOT.TF1( 'funNew', '([0] * x * [1]*[1]*[1]*[1])/( (x*x+[1]*[1])*(x*x+[1]*[1])*(x*x+[1]*[1]) )', mini, maxi)
        if isotropic: funNew = ROOT.TF1( 'funNew', '([0] * x * [1]*[1])/( (x*x+[1]*[1])*(x*x+[1]*[1]) )', mini, maxi)
        f2 = gROOT.GetFunction('funNew')
        f2.SetParameter( 0, fitScale )
        f2.SetParameter( 1, fitDepth )

        c1 = ROOT.TCanvas("c1","title",800,800)
        c1.cd()
        hist.SetBinContent(0, 0)
        hist.SetBinContent(11, 0)
        print "Int: %i" % hist.Integral()
        hist.Draw('hist e1')
        f2.Draw('same')
        fitResult.Draw('same')
        fitResult.SetLineColor(ROOT.kRed)

        chiSq = hist.Chisquare( funNew )

        ''' Build Legend '''
        hist.SetStats(0)
        legend = ROOT.TPaveStats(Max - 5*binWidth, hist.GetMaximum()*0.88, Max, hist.GetMaximum()*1.14 )
        chiSq_ = str( round( chiSq, 3 ) )
        depth_ = str( abs( round(fitDepth, 2) ) )
        uncert_ = str( abs( round(fitDepthError, 2) ) )
        legend.AddText( "Distribution Values" )
        legend.AddText( "Number of Tracks: %i" % hist.Integral() )
        legend.AddText( "Depletion Depth (pixel lengths): %s #pm %s" % (depth_, uncert_) )
        legend.AddText( "Chi Square Value: %s" % chiSq_ )
        legend.Draw()


        #hist.SetMaximum( fitScale * 1.2 )
        sufix = "Sea Level Muon Distribution"
        if isotropic: sufix = "Isotropic Distribution"
        hist.SetTitle('%s %s Fit' % (titleName, sufix))
        hist.GetXaxis().SetRange( 2, 10 )
        c1.SaveAs('%s/%s_%s_%i-%i.png' % (folder, saveName, fitCode, mini, maxi) )
        c1.SaveAs('%s/%s_%s_%i-%i.pdf' % (folder, saveName, fitCode, mini, maxi) )
        #c1.SaveAs('%s/%s_%s_tall_%i-%i.png' % (folder, saveName, fitCode, mini, maxi) )
        ''' store results for a nice print out summary '''
        storage.append( [mini, maxi, fitScale, fitScaleError, abs(fitDepth), fitDepthError, chiSq, accurate] )
        print "\n"
        c1.Close()
        gROOT.cd()

ofile = open('%s/%s_%s.txt' % (folder, saveName, fitCode), 'w')

for line in storage:
    line =  "x range: %3i-%3i  scale: %8i+-%8i  depth: %10f+-%10f   ChiSq: %6f   accurate: %7s" % (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
    print line
    ofile.write("%s\n" % line)

ofile.close()
gROOT.cd()
#gROOT.cd()


