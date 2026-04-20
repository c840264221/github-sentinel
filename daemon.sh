#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

PYTHON="$BASE_DIR/.venv/Scripts/python"
MODULE="app.daemon_main"

PID_FILE="$BASE_DIR/daemon.pid"
LOG_FILE="$BASE_DIR/daemon.log"

start() {
    echo "🚀 启动服务..."

    cd "$BASE_DIR" || exit 1

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "⚠️ 服务已在运行 (PID: $PID)"
            return
        else
            echo "⚠️ 检测到残留 PID 文件，清理..."
            rm -f "$PID_FILE"
        fi
    fi

    nohup "$PYTHON" -m "$MODULE" > "$LOG_FILE" 2>&1 &

    PID=$!
    echo "$PID" > "$PID_FILE"

    sleep 1

    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ 启动成功 (PID: $PID)"
    else
        echo "❌ 启动失败，日志如下："
        cat "$LOG_FILE"
    fi
}

stop() {
    echo "🛑 停止服务..."

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")

        if ps -p "$PID" > /dev/null 2>&1; then
            kill "$PID"
            echo "⏳ 正在停止 (PID: $PID)..."
            sleep 1

            if ps -p "$PID" > /dev/null 2>&1; then
                echo "⚠️ 进程仍在运行，强制终止"
                kill -9 "$PID"
            fi

            echo "✅ 已停止"
        else
            echo "⚠️ 进程不存在"
        fi

        rm -f "$PID_FILE"
    else
        echo "⚠️ 没有 PID 文件"
    fi
}

restart() {
    echo "🔄 重启服务..."
    stop
    sleep 1
    start
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")

        if ps -p "$PID" > /dev/null 2>&1; then
            echo "✅ 服务正在运行 (PID: $PID)"
        else
            echo "❌ PID 文件存在但进程未运行"
        fi
    else
        echo "❌ 服务未运行"
    fi
}

logs() {
    if [ -f "$LOG_FILE" ]; then
        echo "📄 实时日志 (Ctrl+C 退出)"
        tail -f "$LOG_FILE"
    else
        echo "⚠️ 日志文件不存在"
    fi
}

case "$1" in
    start) start ;;
    stop) stop ;;
    restart) restart ;;
    status) status ;;
    logs) logs ;;
    *)
        echo "用法: $0 {start|stop|restart|status|logs}"
        ;;
esac