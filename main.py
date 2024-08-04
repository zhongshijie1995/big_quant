from task import collector, holder

if __name__ == '__main__':
    codes = [
        'SA2409',
        'RM2409',
        'CS2409',
    ]
    collector.Collector().min_line_save_every_day(codes)
    holder.Holder().scheduler_keep()
