import sys
import random
import collections
def gettranslationhash():
        translate={'(1, 2)':[0,0],'(1, 3)':[1,0],'(1, 5)':[2,0],'(1, 7)':[3,0],'(2, 4)':[0,1],'(3, 4)':[1,1],'(3, 5)':[2,1],'(3, 7)':[3,1],'(2, 6)':[0,2],'(4, 6)':[1,2],'(5, 6)':[2,2],'(5, 7)':[3,2],'(2, 8)':[0,3],'(4, 8)':[1,3],'(6, 8)':[2,3],'(7, 8)':[3,3]}
        return translate

def load_file(file):
        tr=gettranslationhash()
        content=[]
        for i in range(1,5):
                content.append([0,0,0,0])
                
        for l in open(file):
                if(l.startswith("to") or l.startswith("min")):
                        continue
                l=l.rstrip("\n")
                a=l.split("\t")
                key=a[0]
                p=tr[key]
                cor=float(a[5])
                content[p[0]][p[1]]=cor
        return content

input=sys.argv[1]
c=load_file(input)

for t in c:
        format="\t".join([str(i) for i in t])
        print format
    
    


"""
to compare [(1, 2), (3, 4), (5, 6), (7, 8), (1, 3), (2, 4), (1, 5), (2, 6), (1, 7), (2, 8), (3, 5), (4, 6), (3, 7), (4, 8), (5, 7), (6, 8)]
min coverage 10
min count 1
(1, 2)	451503	8873.88035697	8860.49865534	7961.26550658	0.897834400346
(7, 8)	454832	8922.07705689	8924.26408792	8022.87747429	0.899106149482
(1, 3)	450071	8857.94666829	8861.1016503	7928.45979202	0.894908098352
(4, 6)	450235	8858.79896249	8887.31720623	7941.32905793	0.89499462718
(4, 8)	450609	8861.43461075	8875.99790751	7937.8521231	0.895039887026
(5, 6)	454075	8908.50933204	8934.776519	8013.718017	0.898234413453
(2, 8)	452614	8876.69260993	8896.97866212	7977.72848949	0.897702400774
(5, 7)	454374	8913.13196845	8918.24178534	8001.73166075	0.897489122238
(1, 5)	452660	8889.02237841	8891.5145175	7977.12443018	0.897287247874
(2, 6)	452160	8869.55555411	8908.27863168	7980.91140689	0.897851814332
(1, 7)	452826	8889.74152309	8898.13512447	7982.71280908	0.897545430067
(3, 7)	452130	8889.99905091	8891.86166742	7967.09685203	0.8960925993
(3, 5)	452171	8890.33060837	8887.3574703	7961.46698887	0.895669567942
(3, 4)	449291	8854.70105666	8846.90905824	7932.09469745	0.896200448935
(2, 4)	449444	8838.42380218	8848.23403855	7917.70449914	0.895330908577
(6, 8)	453649	8929.96517958	8912.43701503	8008.8880283	0.897736953307
"""

