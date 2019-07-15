import pandas, xlsxwriter, progressbar, datetime

def export(storage):
    now = datetime.datetime.now()
    filename = "bikescrape-%d-%d-%d-%d%d%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    writer = pandas.ExcelWriter('%s.xlsx' % filename, engine='xlsxwriter')
    empty = True
    for city in storage:
        if storage[city] != []:     # ignore empty cities
            empty = False
            export = pandas.DataFrame(data=storage[city], columns=['Listing', 'Price', 'Link', 'Region'])
            export.to_excel(writer, sheet_name='Listings', index=False)
            worksheet = writer.sheets['Listings']
            worksheet.set_default_row(30)
            worksheet.set_column(0, 0, 45)
            worksheet.set_column(1, 1, 8)
            worksheet.set_column(2, 2, 80)
            worksheet.set_column(3, 3, 25)
    if empty == False:
        writer.book.formats[0].set_text_wrap(True)
        print("Exporting to %s.xlsx" % filename)
        writer.save()
        return ("%s.xlsx" %filename)
    else:
        print("Nothing to export :(")
        return None