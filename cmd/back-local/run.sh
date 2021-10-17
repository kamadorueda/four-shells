function main {
  echo '[INFO] Launching local back-end server!' \
    && echo '[WARNING] Please be aware that login functionality wont work' \
    && echo \
    && ./back/bin \
      server \
      --aws-access-key-id "${AWS_ACCESS_KEY_ID_SERVER:-test}" \
      --aws-cloudfront-domain "${AWS_CLOUDFRONT_DOMAIN:-test}" \
      --aws-region "${AWS_REGION:-us-east-1}" \
      --aws-secret-access-key "${AWS_SECRET_ACCESS_KEY_SERVER:-test}" \
      --host 'localhost' \
      --port '8400' \
      --session-secret "${SERVER_SESSION_SECRET:-test}"

}

main "${@}"
