function main {
      echo '[INFO] Launching local back-end server!' \
  &&  echo '[WARNING] Please be aware that login functionality wont work' \
  &&  echo \
  &&  AWS_ACCESS_KEY_ID_SERVER='test' \
      AWS_CLOUDFRONT_DOMAIN='test' \
      AWS_REGION='us-east-1' \
      AWS_SECRET_ACCESS_KEY_SERVER='test' \
      GOOGLE_OAUTH_CLIENT_ID_SERVER='test' \
      GOOGLE_OAUTH_SECRET_SERVER='test' \
      SERVER_SESSION_SECRET='test' \
      ./bin/4s \

}

main "${@}"
