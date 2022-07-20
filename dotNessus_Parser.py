import xml.etree.ElementTree as ET
import sys

myDict={} #dictonary where ports and hosts will be saved




def makeReport(htmlContent):
	f 		=  open("Report.html","w+")  #Report.html will be created in the current directory
	f.write(htmlContent)
	f.close()


def RemoveDup(duplicate):  # Function to remove dups from list
    final_list		= [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    
    return(final_list)



def parseNessusFile(nessusFile):

	f 				= open(nessusFile, 'r')
	xml_content 	= f.read()
	f.close()
	root 			= ET.fromstring(xml_content)


	for block in root:
	    if block.tag 		== "Report":
	        for report_host in block:
	            host_properties_dict 		= dict()
	            for report_item in report_host:

	                if report_item.tag		 == "HostProperties":
	                    for host_properties in report_item:

	                        host_properties_dict[host_properties.attrib['name']] = host_properties.text
	            for report_item in report_host:

	                if 'pluginName' in report_item.attrib:
	                  #  vulner_id = report_host.attrib['name'] + "|" + report_item.attrib['port']  + "|"  +  report_item.attrib['protocol']
	                    if report_host.attrib['name'] not in myDict:
	                        myDict[report_host.attrib['name']] = []
	                    else:
	                        myDict[report_host.attrib['name']].append(report_item.attrib['port'])
	                    # myDict[report_host.attrib['name']] = report_item.attrib['port']
	                    # print(report_host.attrib['name'] +"|"+ report_item.attrib['port'])

	htmlPage='''
	<!DOCTYPE html>
	<html>
	<head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-alpha.4/css/materialize.min.css">
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

	  <script type = "text/javascript" src = "https://code.jquery.com/jquery-2.1.1.min.js"></script>           
	   <!-- Compiled and minified JavaScript -->
	    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-alpha.4/js/materialize.min.js"></script>
	           

	</head>

	<body class="#37474f blue-grey darken-3"> 
	<div class="container">
	 <ul class="collapsible popout">
	'''

	for _IP in myDict:
	    htmlPage += '''
	    <li>
	     <div class="collapsible-header"><i class="material-icons">expand_more</i>'''+_IP+'''</div>
	    <div class="collapsible-body">
	    '''
	    myDict[_IP].sort()
	    portNumList = RemoveDup(myDict[_IP])
	    for portNum in portNumList:
	        htmlPage +='<div class="chip #64ffda teal accent-2">'+portNum+"</div>"
	    htmlPage += '''
	     </div>
	    </li>'''

	htmlPage += '''
	</ul>
	</div>
	<script>
	  $(document).ready(function(){
	    $('.collapsible').collapsible();
	  });
	</script>
	</body>   
	</html>
	'''
	makeReport(htmlPage)
	print("\n Report.html file created in current directory. Open it in your browser and enjoy :)")



if __name__	==	'__main__':
	if( len(sys.argv) < 2 ):
		print("\n[+] You did not specify a file to parse.\n\nUsage:\n# python3 "+sys.argv[0]+" ScanFile.nessus")
	else:
		parseNessusFile(sys.argv[1])




