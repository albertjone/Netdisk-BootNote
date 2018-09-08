import oss2
from config import oss_setting as alioss


def get_endpoint(protocol, region, domain):
    return protocol + "://" + region + "." + domain


def main():
    endpoint = get_endpoint(alioss.protocol,
                            alioss.regions['huadong-2'],
                            alioss.domain)
    auth = oss2.Auth(alioss.AccessKeyID, alioss.AccessKeySecret)
    bucket = oss2.Bucket(auth, endpoint, 'netdisk-g-notebook')
    key = 'story.txt'
    bucket.put_object(key, 'Ali baba is a happy youth')
    bucket.get_object(key).read()


if __name__ == "__main__":
    main()
