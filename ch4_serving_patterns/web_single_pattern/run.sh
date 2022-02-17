#!/bin/bash

# set -e: 실패시 남아있는 명령을 실행하지 않게함
# set -u: 정의되지 않은 변수를 참조시 에러 출력
set -eu

HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-4}  # worker process 수
UVICORN_WORKER=${UVICORN_WORKER:-"uvicorn.workers.UvicornWorker"}  # worker class: uvicorn worker
LOGLEVEL=${LOGLEVEL:-"debug"}
LOGCONFIG=${LOGCONFIG:-"./src/utils/logging.conf"}
BACKLOG=${BACKLOG:-2048}  # 서비스를 받기 위해 대기할 수 있는 클라이언트 수
LIMIT_MAX_REQUESTS=${LIMIT_MAX_REQUESTS:-65536}  # 재시작하기 전에 워커가 처리할 최대 요청 수
MAX_REQUESTS_JITTER=${MAX_REQUESTS_JITTER:-2048}  # 모든 워커가 동시에 재시작하지 않도록 재시작 가능 수 제한
GRACEFUL_TIMEOUT=${GRACEFUL_TIMEOUT:-10}  # 정상인 워커의 재시작 시간
APP_NAME=${APP_NAME:-"src.app.app:app"}

gunicorn ${APP_NAME} \
    -b ${HOST}:${PORT} \
    -w ${WORKERS} \
    --worker-class ${UVICORN_WORKER} \
    --log-level ${LOGLEVEL} \
    --log-config ${LOGCONFIG} \
    --backlog ${BACKLOG} \
    --max-requests ${LIMIT_MAX_REQUESTS} \
    --max-requests-jitter ${MAX_REQUESTS_JITTER} \
    --graceful-timeout ${GRACEFUL_TIMEOUT} \
    --reload  # for only dev, 코드 변경되면 재실행
