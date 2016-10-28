DACscan_range0_5k = range(20,130,2) + range(130,550,5)
#DACscan_range0_1k = range(20,110)
DACscan_range1_1k = range(75,120,5)+range(125,411,5)+range(420,741,10)
DACscan_range2_1k = range(3050,6021,80)#range(700,1201,20)+range(1250,2011,40)+range(2050,3001,60)+range(3050,6021,80)
DACscan_range3_1k = range(5500,8000,200)+range(8000,20251,300)+range(25000,35001,400)+range(38000,48000,500)

#DACscan_range0_5k = [50,150,400,550]
#DACscan_range0_1k = [40,55,70,85]
#DACscan_range1_1k = [70, 200, 400, 700]
#DACscan_range2_1k = [700, 1500, 3000, 6000]
#DACscan_range3_1k = [10000, 20000, 30000, 40000]

scanValues = { 0 : DACscan_range0_5k ,
               1 : DACscan_range1_1k ,
               2 : DACscan_range2_1k ,
               3 : DACscan_range3_1k ,
               }

DACscan_range0_1k_shunt = range(30,100,2)
DACscan_range1_1k_shunt = range(75,750,15)
DACscan_range2_1k_shunt = range(800,6000,100)
DACscan_range3_1k_shunt = range(6000,45000,1000)


#DACscan_range0_1k_shunt = [30,50,70,100]
#DACscan_range1_1k_shunt = [100,250,400,650]
#DACscan_range2_1k_shunt = [1000, 2500, 4000, 6000]
#DACscan_range3_1k_shunt = [6000,12000, 24000,40000]


scanValues_shunt = [DACscan_range0_1k_shunt,
                    DACscan_range1_1k_shunt,
                    DACscan_range2_1k_shunt,
                    ]

