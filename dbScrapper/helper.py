# Helper Functions to read the specific table columns

def get_train(row):
    return row.css('td.train a::text').get()


def get_route(row):
    try:
        route = row.css('td.route::text').getall()[2]
    except:
        route = ''

    return ''


def get_platform(row):
    platform = row.css('td.platform strong::text').get()
    if platform is None:
        platform = row.css('td.platform strong span.red::text').get()
        if platform is None:
            try:
                platform = row.css('td.platform::text').getall()[1]
            except:
                platform = ''
    return platform


def get_delay_time(row):
    delayTime = row.css('td.ris span.delay.bold::text').get()

    if delayTime == '':
        delayTime = row.css('td.ris span.red::text').get()
        result['information'] = row.css('td.ris span.delay.bold::text').get()

    return delayTime


def get_delay_info(row):
    delayTime = row.css('td.ris span.delay.bold::text').get()

    if delayTime == '':
        delayTime = row.css('td.ris span.red::text').get()
        result['information'] = row.css('td.ris span.delay.bold::text').get()

    return delayTime
