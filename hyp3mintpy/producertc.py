from hyp3_sdk import HyP3

hyp3 = HyP3(username='cirrusasf', password='Cumulus*181')

granule = 'S1A_IW_SLC__1SSV_20150621T120220_20150621T120232_006471_008934_72D8'

granule = 'S1A_IW_SLC__1SSV_20160205T205112_20160205T205139_009816_00E5D1_997E'

job = hyp3.submit_rtc_job(granule=granule, name='jz-rtc-1', include_dem=True)

job = hyp3.watch(job)

job.download_files()
