.PHONY: aws-assets

gcloud-assets:
	#aws s3 sync dev s3://trendspotting.site/2020/June/breeds --delete --cache-control 'max-age=31536000' --exclude 'index.html' --exclude 'bundle.js'
	gsutil cp ny.html gs://trendspotting_general_storage/trendspotting.sk/ny.html
	# https://storage.cloud.google.com/trendspotting_general_storage/trendspotting.sk/ny.html


# aws-htmljs:
# 	aws s3 cp dev/index.html s3://trendspotting.site/2020/June/breeds/index.html
# 	aws s3 cp dev/bundle.js s3://trendspotting.site/2020/June/breeds/bundle.js

# aws-cache:
# 	aws cloudfront create-invalidation --distribution-id E13X38CRR4E04D --paths '/year/month/name*'	

go: gcloud-assets