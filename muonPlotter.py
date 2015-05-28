#!/usr/bin/env python
################################################################################
# Take output files listed with key words in 'mapper' and plot their 'muon'-like
# values.
################################################################################

import os
from ROOT import gROOT, gStyle
import ROOT
from array import array

nBins = 50
nMax = 100

mapper = { 'HTC_A510' : ('2010', '405', '8025'),#, 's'),
#           'HTC_A510' : '405',
#           'HTC_A510' : '8025',
           'SPH-D710VMUB' : ('2010', '405', '8025'),#('1'),#, 's'),
           #'SAMSUNG-SGH' : ('1')
}

def getPass( name, length, ecc ):
  hallPass = False
  if name == 'HTC_A510':
      if length < 10 and ecc > 0.7:
        hallPass = True
  if 'SPH' in name:
      if length < 10 and ecc > 0.9:
        hallPass = True
  if 'RAZR  ' in name:
      if length < 8 and ecc > 0.7:
        hallPass = True
  return hallPass

def getRecord(ifile):
  record = {}
  count = 0
  previous = '0'
  for line in ifile:
      if 'majA' not in line: continue
      info = line.split(' ')
      event = str( info[0] )
      if event == previous:
          count += 1
      else:
          record[ event ] = count
          count = 1
          previous = event
  return record
          
for key in mapper.keys():
  gStyle.SetOptStat( 1 )
  print key

  if 'HTC' in key:
    nBins = 10
    nMax = 100
    lenMax = 30
    fitMin = 4
    namer = "HTC Wildfire S"
  if 'SPH' in key:
    nBins = 10
    nMax = 70
    lenMax = 30
    fitMin = 2
    namer = "Samsumg Galaxy S2"
  if 'RAZR' in key:
    nBins = 20
    nMax = 40 
    lenMax = 20
    fitMin = 3
    namer = "RAZR"

  for name in mapper[key]:
    #ofile = open('muons_%s.txt' % key, 'w')
    #ofile.write('Image : Eccentricites : Len1 : Len 2\n')
    #lHistAll = ROOT.TH1F('%slength1' % namer, '%s, Length of Muon Tracks, ecc = All' % namer, nBins, 0, nMax)
    #lHist90 = ROOT.TH1F('%slength2' % namer, '%s, Length of Muon Tracks, ecc > 0.9' % namer, nBins, 0, nMax)
    #lHist95 = ROOT.TH1F('%slength3' % namer, '%s, Length of Muon Tracks, ecc > 0.95' % namer, nBins, 0, nMax)
    lHist99 = ROOT.TH1F('%slength' % namer, '%s, Length of Muon Tracks, ecc > 0.99' % namer, nBins, 0, nMax)
    #cdf = ROOT.TH1F('%scdf' % namer, '%s, CDF of all events' % namer, nMax, 0, nMax)
    lenVsEcc = ROOT.TH2I('%slenVsEcc' % namer, 'Eccentricity vs. Length', 100/2, 0.0, lenMax, 100/2, 0, 1)
    lenVsEcc2 = ROOT.TH2I('%slenVsEcc2' % namer, 'Eccentricity vs. Length', 100/2, 0.0, lenMax, 100/2, 0.5, 1)
    AreaVsEcc = ROOT.TH2I('%sareaVsEcc' % namer, 'Eccentricity vs. Area', 100/2, 0.0, 100, 100/2, 0, 1)
    AreaVsEcc2 = ROOT.TH2I('%sareaVsEcc2' % namer, 'Eccentricity vs. Area', 100/2, 0.0, 100, 100/2, 0.5, 1)

    print name
#    name = '%s%s' % (key, i)
    ifile = open('%s_log%s.out' % (key, name), 'r')
    record = getRecord( ifile )
    ifile.close()    

    ifile = open('%s_log%s.out' % (key, name), 'r')
    for linex in ifile:
        if 'majA' not in linex: continue
        info = linex.split(' ')
        fst = str( info[0] )[0]
        event = str( info[0] )
        ecc = float( info[12] )
        l1 = float( info[18] )
        l2 = float( info[21] )
        area = float( info[15] )
        majA = float( info[3] )
        minA = float( info[6] )
        #print "majA: %f minA: %f area: %f" % (majA, minA, area)
        #ofile.write('%10s %10f %10f %10f' % (info[0], ecc, l1, l2) )
        len_ = l2

        # Skip the event line if there are more than XXX blobs that were IDed in that image
        if record[ event ] > 1: continue
        #if area > 10 and name == '405': continue
        #if area > 5 and name == '8025': continue

        # Always fill the length vs eccentricity plot
        lenVsEcc.Fill( len_, ecc)
        lenVsEcc2.Fill( len_, ecc)
        AreaVsEcc.Fill( area, ecc)
        AreaVsEcc2.Fill( area, ecc)
 
        # Does the candidate pass the lower eccentricity / vertical candadate cut?
        passing = False
        passing = getPass( key, len_, ecc )
        ''' To return to the Passing option, comment out following line '''
        passing = False

        #cdf.Fill( len_ )
        #lHistAll.Fill( len_ )
        if float( ecc ) > 0.99 or passing:
            lHist99.Fill( len_ )
        #if float( ecc ) > 0.95 or passing:
        #    lHist95.Fill( len_ )
        #if float( ecc ) > 0.90:
        #    lHist90.Fill( len_ )

    #ofile.close()
    ''' Make a CDF plot, I didn't actualy use this at all '''
    #c5 = ROOT.TCanvas("c1","title",600,600)
    #cdfFinal = ROOT.TH1F('%scdfFinal' % key, '%s, CDF of all events' % key, nMax, 0, nMax)
    #for bin in range( 1, nMax + 1 ):
    #    newVal = cdfFinal.GetBinContent( bin - 1 ) + cdf.GetBinContent( bin )
    #    cdfFinal.SetBinContent( bin, newVal )
    #cdfFinal.Scale( 1 / cdfFinal.GetBinContent( nMax ) )
    #cdfFinal.Draw()
    #c5.SaveAs('CDF_%s.png' % key)
    #c5.Close()
  
    ''' Plot all 4 option with eccentricity progression '''
    #c1 = ROOT.TCanvas("c1","title",1200,400)
    #c1.Divide(4,1)
    #c1.cd(1)
    #pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
    #pad1.Draw()
    #pad1.Close()
    #lHistAll.Draw('hist e1')
    #c1.cd(2)
    #pad2 = ROOT.TPad("pad2", "", 0, 0, 1, 1)
    #pad2.Draw()
    #pad2.Close()
    #lHist90.Draw('hist e1')
    #c1.cd(3)
    #pad3 = ROOT.TPad("pad3", "", 0, 0, 1, 1)
    #pad3.Draw()
    #pad3.Close()
    #lHist95.Draw('hist e1')
    #c1.cd(4)
    #pad4 = ROOT.TPad("pad4", "", 0, 0, 1, 1)
    #pad4.Draw()
    #pad4.Close()
    #lHist99.Draw('hist e1')  
    #c1.SaveAs('muonsPlot_%s.png' % key)
    #c1.Close()
    c2 = ROOT.TCanvas("c2","title",600,600)
    lHist99.GetXaxis().SetTitle("Length (pixel widths)")
    lHist99.GetYaxis().SetTitle("Events / %s pixel widths" % str(nMax/nBins) )
    lHist99.Draw('hist e1')
    c2.SaveAs('hist_%s%s.png' % (key, name))
    lHist99.SaveAs('root_%s%s.root' % (key, name))
  
    ''' Do some fitting to find the depth of the depletion region '''
#    #funx = ROOT.TF1( 'funx', '[0] * cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', (nMax/nBins)*fitMin, nMax)
#    funx = ROOT.TF1( 'funx', '[0]*cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', 15, 110)
##$    funx = ROOT.TF1( 'funx', '(1/(1+TMath::Exp([2]*(x-[3]))))*[0] * cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', 0, nMax)
#    f1 = gROOT.GetFunction('funx')
#    f1.SetParName( 0, "vert count" )
#    f1.SetParName( 1, "depth" )
#    f1.SetParameter( 0, 999 )
#    f1.SetParameter( 1, 999 )
##$    f1.SetParName( 2, "steepness" )
##$    f1.SetParameter( 2, -1 )
##$    f1.SetParName( 3, "x offset" )
##$    f1.SetParameter( 3, 3 )
#  
#    lHist99.Fit('funx', 'EMRI')
#    fitResult = lHist99.GetFunction("funx")
#    lHist99.SetAxisRange( 0, nMax )
#    fitResult.Draw('same')
#    c2.SaveAs('final%s%s_Fit.png' % (key, name) )
  
  #  # Plot others varied by for an eye comparison
  #  # Adjust the depth fit to show errors
  #  fitVert = fitResult.GetParameter( 0 )
  #  fitDepth = fitResult.GetParameter( 1 )
  #  fitSteep = fitResult.GetParameter( 2 )
  #  fitOffset = fitResult.GetParameter( 3 )
  #  fitVertError = fitResult.GetParError( 0 )
  #  fitDepthError = fitResult.GetParError( 1 )
  #  fitSteepError = fitResult.GetParError( 2 )
  #  fitOffsetError = fitResult.GetParError( 3 )
  #  fun2 = ROOT.TF1( 'fun2', '(1/(1+TMath::Exp([2]*(x-[3]))))*[0] * cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', 0, nMax)
  #  f2 = gROOT.GetFunction('fun2')
  #  f2.SetParameter( 0, fitVert )
  #  f2.SetParameter( 1, fitDepth + fitDepthError )
  #  #f2.SetParameter( 1, fitDepth * 1.5 )
  #  f2.SetParameter( 2, fitSteep )
  #  f2.SetParameter( 3, fitOffset )
  #  f2.Draw('same')
  #  fun3 = ROOT.TF1( 'fun3', '(1/(1+TMath::Exp([2]*(x-[3]))))*[0] * cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', 0, nMax)
  #  f3 = gROOT.GetFunction('fun3')
  #  f3.SetParameter( 0, fitVert )
  #  f3.SetParameter( 1, fitDepth - fitDepthError )
  #  #f3.SetParameter( 1, fitDepth * 0.5 )
  #  f3.SetParameter( 2, fitSteep )
  #  f3.SetParameter( 3, fitOffset )
  #  f3.Draw('same')
  #  c2.Update()
  #  c2.SaveAs('finalFit%s_depthfit.png' % key)
  #
  #  # Adjust the vertical fit to show errors
  #  f2.SetParameter( 0, fitVert + fitVertError )
  #  #f2.SetParameter( 0, fitVert * 1.5 )
  #  f2.SetParameter( 1, fitDepth )
  #  f3.SetParameter( 0, fitVert - fitVertError )
  #  #f3.SetParameter( 0, fitVert * 0.5 )
  #  f3.SetParameter( 1, fitDepth )
  #  c2.Update()
  #  c2.SaveAs('finalFit%s_vertFit.png' % key)
  #
  #  # Adjust the steepness fit to show errors
  #  f2.SetParameter( 0, fitVert )
  #  #f2.SetParameter( 2, fitSteep + fitSteepError )
  #  f2.SetParameter( 2, fitSteep * 1.5 )
  #  f3.SetParameter( 0, fitVert )
  #  #f3.SetParameter( 2, fitSteep - fitSteepError )
  #  f3.SetParameter( 2, fitSteep * 0.5 )
  #  c2.Update()
  #  c2.SaveAs('finalFit%s_steepFit.png' % key)
  #
  #  # Adjust the offset fit to show errors
  #  f2.SetParameter( 3, fitOffset + fitOffsetError )
  #  f2.SetParameter( 2, fitSteep )
  #  f3.SetParameter( 3, fitOffset - fitOffsetError )
  #  f3.SetParameter( 2, fitSteep )
  #  c2.Update()
  #  c2.SaveAs('finalFit%s_offsetFit.png' % key)
  #  c2.Close()
  
    c3 = ROOT.TCanvas("c3","title",800,800)
    c3.Divide(2,2)
    c3.cd(1)
    lenVsEcc.Draw('COLZ')
    c3.cd(2)
    lenVsEcc2.Draw('COLZ')
    c3.cd(3)
    AreaVsEcc.Draw('COLZ')
    c3.cd(4)
    AreaVsEcc2.Draw('COLZ')
    gStyle.SetOptStat( 0 )
    c3.SaveAs('lenVsEcc_%s%s.png' % (key, name) )
    c3.Close()
  
    gROOT.cd()
