# Helper Functions to read the specific table columns

def get_train(row):
    train = row.css('td.train a::text').getall()

    if len(train) == 0:
        return None
    else:
        if len(train) > 1:
            train_name = row.css('td.train a span.nowrap::text').get()
            train = train_name + ' ' + train[1]
        else:
            train = train[0]

    return train


def get_route(row):
    try:
        route = row.css('td.route::text').getall()[2]
    except:
        route = ''

    return route


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
    delay_time = row.css('td.ris span.delay.bold::text').get()

    if delay_time is None:
        delay_time = row.css('td.ris span.delayOnTime::text').get()

    return delay_time


def get_info(row):
    return row.css('td.ris span.red::text').get()
