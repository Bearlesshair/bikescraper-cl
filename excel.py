import pandas, xlsxwriter, progressbar, datetime

def export(storage):
    now = datetime.datetime.now()
    filename = "bikescrape-%d-%d-%d-%d%d%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    print("Exporting to %s.xlsx" %filename)
    writer = pandas.ExcelWriter('%s.xlsx' % filename, engine='xlsxwriter')
    for city in storage:
        if storage[city] != []:     # ignore empty cities
            export = pandas.DataFrame(data=storage[city], columns=['Listing', 'Price', 'Link'])
            export.to_excel(writer, sheet_name=city.title(), index=False)
            worksheet = writer.sheets[city.title()]
            worksheet.set_default_row(30)
            worksheet.set_column(0, 0, 45)
            worksheet.set_column(1, 1, 8)
            worksheet.set_column(2, 2, 80)
    writer.book.formats[0].set_text_wrap(True)
    writer.save()
