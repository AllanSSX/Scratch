#!/usr/bin/env python

import argparse


def getArgs():
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-c',dest="chain",type=argparse.FileType('r'),required=True,help='Old chain file (V1 -> V2)')
	# parser.add_argument('-f',dest="frags",type=argparse.FileType('r'),required=True,help='Info frags (simplified)')
	parser.add_argument('-l',dest="lifted",type=argparse.FileType('r'),required=True,help='Bed lifted')
	parser.add_argument('-n',dest="name",type=str,required=True,help='New chr name')
	parser.add_argument('-s',dest="size",type=int,required=True,help='Size of the new chr')
	
	
	arg = parser.parse_args()
	
	return arg

def main(args):
	
	chain_infos = {}
	
	# 1 - recuperation des coordonnees dans l'ancien liftOver
	# /!\ recalculer pour les sctg en orientation negative
	"""
	chain	1000	sctg_207	293188	+	0	293188	chr_01	10318834	+	0	293188	1
	293188
	chain	1000	sctg_486	77004	+	0	77004	chr_01	10318834	+	293288	370292	2
	77004
	chain	1000	sctg_516	63439	+	0	63439	chr_01	10318834	+	370392	433831	3
	63439
	chain	1000	sctg_228	263496	+	0	263496	chr_01	10318834	+	433931	697427	4
	263496
	chain	1000	sctg_151	413142	+	0	413142	chr_01	10318834	-	9208165	9621307	5
	413142
	chain	1000	sctg_112	523010	+	0	523010	chr_01	10318834	+	1110769	1633779	6
	523010
	"""
	
	for line in args.chain:
		if line.startswith('chain'):
			chain, score, tName, tSize, tStrand, tStart, tEnd, qName, qSize, qStrand, qStart, qEnd, idIter = line.split()
			# sctg = tName
			
			# if qStrand == '-':
			# 	qStartOK = int(qSize) - int(qEnd)
			# 	qEndOK = int(qSize) -int(qStart)
			# else:
			# 	qStartOK = qStart
			# 	qEndOK = qEnd
			
			# chain_infos[sctg] = {'qtlStart': int(qStartOK), 'qtlEnd':int(qEndOK), 'qtlSize':int(qSize), 'sctgSize': int(tSize)}
		if not qName in chain_infos:
			chain_infos[qName] = {'qtlSize':int(qSize), tName:qStrand}
		else:
			chain_infos[qName][tName] = qStrand
	# check
	# for key, value in chain_infos.items():
	# 	print(key, value)
	# 	
	# exit(0)
	
	# 2 - creation du fichier liftOver
	# /!\ contigs en stand -, calculer les coordonnes depuis la fin du chromosome cible, sauf si deja inverse dans la version qtl
	"""
	chain	1000	sctg_437	101602	+	0	101602	chr_22	4515851	+	0		101602	269
	chain	1000	sctg_162	401382	+	0	401382	chr_22	4515851	+	101702	503084	270
	chain	1000	sctg_65		739199	+	0	739199	chr_22	4515851	+	503184	1242383	271
	chain	1000	sctg_368	155157	+	0	155157	chr_22	4515851	+	1242483	1397640	272
	chain	1000	sctg_179	375655	+	0	375655	chr_22	4515851	+	1397740	1773395	273
	chain	1000	sctg_423	103715	+	0	103715	chr_22	4515851	+	1773495	1877210	274
	chain	1000	sctg_84		599728	+	0	599728	chr_22	4515851	-	2038813	2638541	275
	chain	1000	sctg_528	56950	+	0	56950	chr_22	4515851	+	2477138	2534088	276
	chain	1000	sctg_635	31429	+	0	31429	chr_22	4515851	+	2534188	2565617	277
	chain	1000	sctg_539	50649	+	0	50649	chr_22	4515851	+	2565717	2616366	278
	chain	1000	sctg_91		564433	+	0	564433	chr_22	4515851	+	2616466	3180899	279
	chain	1000	sctg_493	83472	+	0	83472	chr_22	4515851	+	3180999	3264471	280
	chain	1000	sctg_200	306974	+	0	306974	chr_22	4515851	+	3264571	3571545	281
	chain	1000	sctg_572	43298	+	0	43298	chr_22	4515851	+	3571645	3614943	282
	chain	1000	sctg_885	9129	+	0	9129	chr_22	4515851	+	3615043	3624172	283
	chain	1000	sctg_39		891579	+	0	891579	chr_22	4515851	-	0		891579	284
	"""
	
	startPos = 0
	endPos = 0
	iterFrag = 1
	
	for line in args.lifted:
		
		chrQTL, startQTL, endQTL, orientation, sctgName = line.split()

		qtlSize = chain_infos[chrQTL]['qtlSize']
		# qtlStart = chain_infos[chrSCTG]['qtlStart']
		# qtlEnd = chain_infos[chrSCTG]['qtlEnd']
		addSize = int(endQTL) - int(startQTL)
			
		startHiC = startPos
		endHiC = startPos + addSize
	
		if orientation == '1' and chain_infos[chrQTL][sctgName] == '+':
			# print(sctgName)
			orientation = '+'
		elif orientation == '-1' and chain_infos[chrQTL][sctgName] == '-':
			orientation = '+'
		elif orientation == '1' and chain_infos[chrQTL][sctgName] == '-':
			# print(sctgName)
			orientation = '-'
			# transform coordinate from the end of the chromosome
			startHiC = args.size - (startPos + addSize) #endHiC 
			endHiC = args.size - startPos #startHiC
		else:
			orientation = '-'
			# transform coordinate from the end of the chromosome
			startHiC = args.size - (startPos + addSize) #endHiC 
			endHiC = args.size - startPos #startHiC
			
		qtlSize = str(qtlSize)
		qtlStart = str(startQTL)
		qtlEnd = str(endQTL)
			
		print('chain\t1000\t'+chrQTL+'\t'+qtlSize+'\t+\t'+qtlStart+'\t'+qtlEnd+'\t'+args.name+'\t'+str(args.size)+'\t'+orientation+'\t'+str(startHiC)+'\t'+str(endHiC)+'\t'+str(iterFrag))
		print(str(addSize))
		print('')
			
		startPos += addSize
		iterFrag += 1
	
if __name__ == '__main__':
	args = getArgs()
	main(args)
