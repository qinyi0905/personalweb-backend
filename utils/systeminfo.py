import time, re
import config
import datetime


class SystemInfo:

    def get_cpu_usage(self):
        try:
            with open(config.CPU_INFO_PATH, 'r') as f:
                line = f.readline().split()
                user1 = int(line[1])
                nice1 = int(line[2])
                system1 = int(line[3])
                idle1 = int(line[4])
                iowait1 = int(line[5])
                irq1 = int(line[6])
                softirq1 = int(line[7])

            # Wait 1 second
            time.sleep(1)

            # Read second sample
            with open(config.CPU_INFO_PATH+"1", 'r') as f:
                line = f.readline().split()
                user2 = int(line[1])
                nice2 = int(line[2])
                system2 = int(line[3])
                idle2 = int(line[4])
                iowait2 = int(line[5])
                irq2 = int(line[6])
                softirq2 = int(line[7])

        except Exception as e:
            return 0.00

        # Calculate differences
        total1 = user1 + nice1 + system1 + idle1 + iowait1 + irq1 + softirq1
        total2 = user2 + nice2 + system2 + idle2 + iowait2 + irq2 + softirq2
        total_diff = total2 - total1
        idle_diff = idle2 - idle1

        # Calculate CPU usage
        if total_diff == 0:
            return 0.0
        else:
            return f"{(100.0 * (total_diff - idle_diff) / total_diff):.2f}"

    def get_memory_usage(self):
        mem_info = {}

        try:
            with open(config.MEM_INFO_PATH, 'r') as f:
                for line in f:
                    parts = line.split()
                    if parts[0] == 'MemTotal:':
                        mem_info['total'] = int(parts[1]) / 1024  # Convert KB to MB
                    elif parts[0] == 'MemFree:':
                        mem_info['free'] = int(parts[1]) / 1024
                    elif parts[0] == 'MemAvailable:':
                        mem_info['available'] = int(parts[1]) / 1024
        except Exception as e:
            return 0.00

        # Calculate used memory and usage percentage
        if 'total' in mem_info and 'available' in mem_info:
            mem_info['used'] = mem_info['total'] - mem_info['available']
            mem_info['usage_percent'] = (mem_info['used'] / mem_info['total']) * 100

        return f"{mem_info['usage_percent']:.2f}"

    def get_nginx_access_log(self):
        date_access = {}
        today = datetime.datetime.now()
        for i in range(7):
            target_date = today - datetime.timedelta(days=i)
            date_key = target_date.strftime("%d/%b/%Y")
            date_access[date_key] = 0
        try:
            with open(config.NGINX_ACCESS_LOG_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    match = re.search(r'\[(\d{2}/[A-Za-z]{3}/\d{4}):', line)
                    if match:
                        log_date = match.group(1)
                        if log_date in date_access:
                            date_access[log_date] += 1
            return date_access
        except Exception as e:
            return date_access

# Example usage
if __name__ == "__main__":
    sys_info = SystemInfo()

    print(sys_info.get_cpu_usage())
