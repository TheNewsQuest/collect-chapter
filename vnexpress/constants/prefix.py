from vnexpress.enums.categories import VNExpressCategories

VNEXPRESS_BUCKET_PREFIX = "vnexpress"
NEWS_BUCKET_PREFIX = f"{VNEXPRESS_BUCKET_PREFIX}/{VNExpressCategories.NEWS}"
BUSINESS_BUCKET_PREFIX = f"{VNEXPRESS_BUCKET_PREFIX}/{VNExpressCategories.BUSINESS}"
LIFE_BUCKET_PREFIX = f"{VNEXPRESS_BUCKET_PREFIX}/{VNExpressCategories.LIFE}"
