module.exports = {
    apps: [
        {
            name: "dex-futures-bot",
            script: "./main.py",
            interpreter: "./.venv/bin/python3",
            cwd: "/root/scripts/dex-futures-bot",
            watch: false,
            error_file: "/root/.pm2/logs/dex-futures-bot-error.log",
            out_file: "/root/.pm2/logs/dex-futures-bot-out.log",
            pid_file: "/root/.pm2/pids/dex-futures-bot.pid",
            exec_mode: "fork",
            env: {
                NODE_ENV: "production",
            },
            log_date_format: "YYYY-MM-DD HH:mm:ss",
            max_size: "10M",
            merge_logs: true,
            // cron_restart: "0 6 * * *", // Убрано, чтобы скрипт никогда не перезапускался
            autorestart: false
        },
    ],
};