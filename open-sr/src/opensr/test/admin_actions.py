import csv
import codecs
import cStringIO
from StringIO import StringIO  
from zipfile import ZipFile  
from django.http import HttpResponse
from test.models import Trial

export_info = [
    ("Date", "date"),
    ("Time", "time"),
    ("Test", "test__test_name"),
    ("Group", "group"),
    ("Block", "block"),
    ("Practice", "practice"),
    ("Primary Left Category", "primary_left_category"),
    ("Secondary Left Category", "secondary_left_category"),
    ("Primary Right Category", "primary_right_category"),
    ("Secondary Right Category", "secondary_right_category"),
    ("Anchor", "anchor"),
    ("Latency", "latency"),
    ("Correct", "correct"),
]

class UnicodeWriter:
    
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            
def export_as_csv(modeladmin, request, queryset):
    headers, fields = zip(*export_info)     
    in_memory = StringIO()  
    zipFile = ZipFile(in_memory, 'a')  
    for participant in queryset:
        rows = [headers]
        trials = Trial.objects.filter(participant=participant.id)
        for trial_value_list in trials.values_list(*fields):
            rows.append([unicode(v) for v in trial_value_list])
        
        f = StringIO()
        writer = UnicodeWriter(f)
        for row in rows:
            writer.writerow(row)
            
        zipFile.writestr('%s-participant-%d.csv' % (participant.test.test_name.lower(), participant.id), f.getvalue())  
        
    for file in zipFile.filelist:  
        file.create_system = 0      
    
    zipFile.close()
    
    response = HttpResponse(mimetype='application/zip')  
    response['Content-Disposition'] = 'attachment; filename=results.zip'
    
    in_memory.seek(0)      
    response.write(in_memory.read())
    
    return response    

export_as_csv.short_description = "Export as CSV"