library("readxl")
library(tidyverse)

# POA Data is demographics based on postcode
poa_directory = "2016_GCP_ALL_for_Vic_short-header/2016 Census GCP All Geographies for VIC/POA/VIC/"

# Age Diversity
main_dataset = NULL
dat = read.csv(file = paste(poa_directory,"2016Census_G04A_VIC_POA.csv", sep=''), header=TRUE)
main_dataset = cbind(main_dataset, postcode=substr(dat$POA_CODE_2016,4,8))

main_dataset = cbind(main_dataset, age_0_14=dat$Age_yr_0_4_P + dat$Age_yr_5_9_P + dat$Age_yr_10_14_P)
main_dataset = cbind(main_dataset, age_15_24=dat$Age_yr_15_19_P + dat$Age_yr_20_24_P)
main_dataset = cbind(main_dataset, age_25_34=dat$Age_yr_25_29_P + dat$Age_yr_30_34_P)
main_dataset = cbind(main_dataset, age_35_44=dat$Age_yr_35_39_P + dat$Age_yr_40_44_P)
main_dataset = cbind(main_dataset, age_45_54=dat$Age_yr_45_49_P + dat$Age_yr_50_54_P)

dat = read.csv(file = paste(poa_directory,"2016Census_G04B_VIC_POA.csv", sep=''), header=TRUE)
main_dataset = cbind(main_dataset, age_55_64=dat$Age_yr_55_59_P + dat$Age_yr_60_64_P)
main_dataset = cbind(main_dataset, age_65_74=dat$Age_yr_65_69_P + dat$Age_yr_70_74_P)
main_dataset = cbind(main_dataset, age_75_84=dat$Age_yr_75_79_P + dat$Age_yr_80_84_P)
main_dataset = cbind(main_dataset, age_85_plus=dat$Age_yr_85_89_P + dat$Age_yr_90_94_P + dat$Age_yr_95_99_P + dat$Age_yr_100_yr_over_P)
main_dataset = cbind(main_dataset, tot_P=dat$Tot_P)

main_dataset = as.data.frame(main_dataset)

# Cultural Diversity
# Parent born overseas
dat = read.csv(file = paste(poa_directory,"2016Census_G08_VIC_POA.csv", sep=''), header=TRUE)
temp = dat$Tot_P_BP_B_OS + dat$Tot_P_BP_B_Aus + dat$Tot_P_FO_B_OS + dat$Tot_P_MO_B_OS
main_dataset = main_dataset %>% cbind(both_par_os=dat$Tot_P_BP_B_OS/temp) %>% 
  cbind(both_par_aus=dat$Tot_P_BP_B_Aus/temp) %>% 
  cbind(f_only_os=dat$Tot_P_FO_B_OS/temp) %>% 
  cbind(m_only_os=dat$Tot_P_MO_B_OS/temp)

# Person born overseas
dat = read.csv(file = paste(poa_directory,"2016Census_G09F_VIC_POA.csv", sep=''), header=TRUE)
born_aus = dat$P_Australia_Tot
dat = read.csv(file = paste(poa_directory,"2016Census_G09H_VIC_POA.csv", sep=''), header=TRUE)
born_os = dat$P_Tot_Tot - dat$P_COB_NS_Tot - born_aus

# Proxy for diversity
# Weights: 
w_both_par_os = 3
w_one_par_os = 1.5
w_born_os = 5
diversity = w_both_par_os*main_dataset$both_par_os + w_one_par_os*(main_dataset$f_only_os+main_dataset$m_only_os) + w_born_os*born_os

main_dataset = main_dataset %>% cbind(born_aus=born_aus/(born_aus+born_os)) %>% 
  cbind(born_os=born_os/(born_aus+born_os)) %>% 
  cbind(diversity = diversity)


# Adding coordinates
dat = read.csv(file = paste("Postcodes/Australian_Post_Codes_Lat_Lon.csv", sep=''), header=TRUE)
main_dataset = main_dataset %>% merge(dat[c('postcode', 'suburb', 'lat', 'lon')], by = "postcode")

# Writing data to CSV
write.csv(main_dataset,'suburb_data.csv')
