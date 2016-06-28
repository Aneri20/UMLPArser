import os
import sys
import plyj.parser as plyj
import requests
import types
import urllib
import glob
sys.path.insert(0,os.environ['Uml_Parser']+"plyj")
os.chdir(str(sys.argv[1]))

main_string = ""
arefType={"name":"","acName":"","relation":""}
arefVar=list()
amParam=list()
aiList=set()
avList = set()
accessors=""
am_name = set()
acList = list()

def acaMods(aclass_interface,main_string):
	try:
		amod_list=aclass_interface.modifiers
		for aMod_count in range(len(amod_list)):
			pass
		return ""
	except ValueError:
		return ""	
		
def type_declarations(aclass_interface,main_string):
	try:
		if str(type(aclass_interface))=="<class 'plyj.model.InterfaceDeclaration'>" :
			aiList.add(aclass_interface.name)
			main_string+="[<<interface>>;"+aclass_interface.name
		else:

			acList.append(aclass_interface.name)
			main_string+="["+aclass_interface.name
		return main_string	
	except ValueError:
		return main_string	

def ainterImpl(aclass_interface,main_string):
	try:
		if str(type(aclass_interface))=="<class 'plyj.model.InterfaceDeclaration'>" :
			pass
		else :
			if aclass_interface.implements:
				aimpl_List=aclass_interface.implements
				for implements_count in range(len(aimpl_List)):
					arefVar.append({"name":aimpl_List[implements_count].name.value,"acName":aclass_interface.name,"relation":"^-.-"})
		return main_string		
	except ValueError:
		return main_string
		
def aext_Classes(aclass_interface,main_string):
	try:
		if aclass_interface.extends:
			extends=aclass_interface.extends
			if str(type(aclass_interface))=="<class 'plyj.model.InterfaceDeclaration'>" :
				arefVar.append({"name":extends.name.value,"acName":aclass_interface.name,"relation":"-.->"})
			else :
				arefVar.append({"name":extends.name.value,"acName":aclass_interface.name,"relation":"^-"})

		return main_string
	except ValueError:
		return main_string	

def aMod(body,accessors):
	try:
		aMod=body.modifiers
		for aMod_count in range(len(aMod)):
			if(aMod[aMod_count] == "private"):
				accessors='-'
			if(aMod[aMod_count] == "public"):
				accessors='+'
			if(aMod[aMod_count] == "protected"):
				accessors='#'
		return accessors
	except ValueError:
		return accessors		

def asetModVar(name):
	try:
		get = 0;
		asetter = 0;
		for am_name_count in am_name:
			if am_name_count.lower()=="get"+name.lower():
				get=1
			if am_name_count.lower()=="asetter"+name.lower():
				asetter=1
		return (get,asetter)		
	except ValueError:
		return (get,asetter)
		
def adata_mem(body,main_string):	
	global ac_var
	if ac_var == 0:			
		try:
			if str(type(body.type))=="<class 'plyj.model.Type'>" :
				main_string=atype_arg_list(body,main_string)
			else :
				avar_dec_list=body.variable_declarators
				for avar_count in range(len(avar_dec_list)):
					avList.add(avar_dec_list[avar_count].variable.name)
					name=avar_dec_list[avar_count].variable.name
					(get,asetter)=asetModVar(name)
					if (get == 1 and asetter == 1):
						main_string+="|+"+name+":"+str(body.type)+";"
						ac_var+=1
					else:
						main_string+="|"+accessors+name+":"+str(body.type)+";"
						ac_var+=1
			return main_string
		except ValueError:
			return main_string
	else:			
		try:
			if str(type(body.type))=="<class 'plyj.model.Type'>" :
				main_string=atype_arg_list(body,main_string)
			else :
				avar_dec_list=body.variable_declarators
				for avar_count in range(len(avar_dec_list)):
					avList.add(avar_dec_list[avar_count].variable.name)
					name=avar_dec_list[avar_count].variable.name
					(get,asetter)=asetModVar(name)
					if (get == 1 and asetter == 1):
						main_string+="+"+name+":"+str(body.type)+";"
					else:
						main_string+=accessors+name+":"+str(body.type)+";"
			return main_string
		except ValueError:
			return main_string			
					
def atype_arg_list(body,main_string):
	try:
		if body.type.type_arguments:				
			aarg_list=body.type.type_arguments
			for argument_count in range(len(aarg_list)):
				avList.add(aarg_list[argument_count].name.value)
				arefVar.append({"name":aarg_list[argument_count].name.value,"acName":aclass_interface.name,"relation":"*"})
		else:
			main_string=avar_dec_list(body,main_string)
			if str(type(body.type.name))=="<class 'plyj.model.Name'>":
				alist=body.type.name
				if alist.value != 'String' :
					avList.add(alist.value)
					arefVar.append({"name":alist.value,"acName":aclass_interface.name,"relation":"1"})
		return main_string		
	except ValueError:
		return main_string			
		

def avar_dec_list(body,main_string):
	global ac_var
	
	if ac_var == 0:
		try:
			avar_list=body.variable_declarators
			for avar_count in range(len(avar_list)):			
				if body.type.dimensions:
					if (body.type.dimensions)==1:
						variable_dimensions='*'
					if (body.type.dimensions)==2:	
						variable_dimensions='**'
					avList.add(avar_list[avar_count].variable.name)	
					name=avar_list[avar_count].variable.name
					(get,asetter)=asetModVar(name)
					if (get == 1 and asetter == 1):
						main_string+="|+"+name+":"+str(body.type.name)+"("+variable_dimensions+")"+";"	
						ac_var+=1	
					else:
						main_string+="|"+accessors+name+":"+str(body.type.name)+"("+variable_dimensions+")"+";"	
						ac_var+=1	
				else:
					avList.add(avar_list[avar_count].variable.name)	
					name=avar_list[avar_count].variable.name
					(get,asetter)=asetModVar(name)
					if (get == 1 and asetter == 1):
						main_string+="|+"+name+":"+str(body.type.name.value)+";"
						ac_var+=1
					else:
						if body.type.name.value=="String":
							main_string+="|"+accessors+name+":"+str(body.type.name.value)+";"
							ac_var+=1
			return main_string
		except ValueError:
			return main_string	

	else:
		try:
			avar_list=body.variable_declarators
			for avar_count in range(len(avar_list)):			
				if body.type.dimensions:
					if (body.type.dimensions)==1:
						variable_dimensions='*'
					if (body.type.dimensions)==2:	
						variable_dimensions='**'
					avList.add(avar_list[avar_count].variable.name)	
					name=avar_list[avar_count].variable.name
					(get,asetter)=asetModVar(name)
					if (get == 1 and asetter == 1):
						main_string+="+"+name+":"+str(body.type.name)+"("+variable_dimensions+")"+";"		
					else:
						main_string+=accessors+name+":"+str(body.type.name)+"("+variable_dimensions+")"+";"		
				else:
					avList.add(avar_list[avar_count].variable.name)	
					name=avar_list[avar_count].variable.name
					(get,asetter)=asetModVar(name)
					if (get == 1 and asetter == 1):
						main_string+="+"+name+":"+str(body.type.name.value)+";"
					else:
						if body.type.name.value=="String":
							main_string+=accessors+name+":"+str(body.type.name.value)+";"
			return main_string
		except ValueError:
			return main_string	
		
def aconst_Dec(body,main_string):
	global acount_meth
	if acount_meth == 0:
		try:
			main_string+="|+"+body.name+"("
			if body.parameters:
				aparam_list=body.parameters
				main_string=parameters(aparam_list,main_string)
			main_string+=");"
			acount_meth+=1
			return main_string	
		except ValueError:
			return main_string
	else:
		try:
			main_string+="+"+body.name+"("
			if body.parameters:
				aparam_list=body.parameters
				main_string=parameters(aparam_list,main_string)
			main_string+=");"
			return main_string	
		except ValueError:
			return main_string

		
def amethod(body,main_string):
	global acount_meth
	if acount_meth == 0:
		try:
			am_name.add(body.name)
			main_string+="|"+accessors+body.name+"("
			if body.parameters:
				aparam_list=body.parameters
				main_string=parameters(aparam_list,main_string)
			
			main_string=return_type(body,main_string)
			acount_meth+=1
			abody_list=body.body
			for abody_count in range(len(abody_list)):
				body=abody_list[abody_count]	
				if str(type(body))=="<class 'plyj.model.VariableDeclaration'>":	
					if body.type.name.value != "String":
						amParam.append({"name":body.type.name.value,"acName":aclass_interface.name,"relation":"1"})
			return main_string
		except ValueError:
			return main_string


	else:
		try:
			am_name.add(body.name)
			main_string+=accessors+body.name+"("
			if body.parameters:
				aparam_list=body.parameters
				main_string=parameters(aparam_list,main_string)
			main_string=return_type(body,main_string)	
			if str(type(body.body))=="<class 'plyj.model.VariableDeclaration'>" :
				if body.type.name.value != "String":
						amParam.append({"name":body.type.name.value,"acName":aclass_interface.name,"relation":"1"})
			return main_string
		except ValueError:
			return main_string

def return_type(abody1,main_string):
	try:
		if str(type(abody1.return_type))=="<class 'plyj.model.Type'>" :				
			main_string+="):"+str(abody1.return_type.name.value)+";"

		else:
			main_string+="):"+abody1.return_type+";"						
		return main_string
	except ValueError:
		return main_string
		
def method_abody(method_abody1,main_string):
	try:

		return main_string
	except ValueError:
		return main_string		
		
def parameters(aparam_list,main_string):
	try:
		
		for aparam_count in range(len(aparam_list)):
			if str(type(aparam_list[aparam_count].type))== "<class 'plyj.model.Type'>" :
				if aparam_list[aparam_count].type.type_arguments:				
					aarg_list=aparam_list[aparam_count].type.type_arguments
					for argument_count in range(len(aarg_list)):
						main_string+= aparam_list[aparam_count].variable.name+":"+aarg_list[argument_count].name.value
						amParam.append({"name":aarg_list[argument_count].name.value,"acName":aclass_interface.name,"relation":"*"})
				else:
					main_string+= aparam_list[aparam_count].variable.name+":"+aparam_list[aparam_count].type.name.value
					if aparam_list[aparam_count].type.name.value != 'String' :
						amParam.append({"name":aparam_list[aparam_count].type.name.value,"acName":aclass_interface.name,"relation":"1"})
			else :	
				main_string+= aparam_list[aparam_count].variable.name+":"+aparam_list[aparam_count].type
		return main_string
	except ValueError:
		return main_string	

		
def asearch_first(main_string,first,afirstStart,last,alast_start):
	try:
		
		data=""
		aindex_begin = main_string.index( first,afirstStart )
		afirstStart=aindex_begin
		(aindex_begin,aindex_last,data)=asforlastandcompare(main_string,first,afirstStart,last,alast_start)
		if(aindex_begin=="0" and aindex_last=="0"):
			alast_start=0
			afirstStart=afirstStart+len(first)
			(aindex_begin,aindex_last,data)=asearch_first(main_string,first,afirstStart,last,alast_start)
			return (aindex_begin,aindex_last,data)
		else:
			return(aindex_begin,aindex_last,data)
	except ValueError:
		aindex_begin="0"
		aindex_last="0"
		data=""
		return (aindex_begin,aindex_last,data)	

def asforlastandcompare(main_string,first,afirstStart,last,alast_start):
	try:
		data=""
		aindex_last = main_string.index(last,alast_start)
		alast_start=aindex_last
		if (alast_start>afirstStart and alast_start>afirstStart+len(first)):
			
			if (main_string[afirstStart+len(first):alast_start]=="uses -.->" ):
				data="uses -.->"
				return (afirstStart,alast_start,data)
			elif (
				alast_start-(afirstStart+len(first)) <=3 and main_string[afirstStart+len(first):alast_start]!="," and main_string[afirstStart+len(first):alast_start]!="^-.-" and main_string[afirstStart+len(first):alast_start]!="-.->" and main_string[afirstStart+len(first):alast_start]!="^-" 
				):
				data="FL"
				return (afirstStart,alast_start,data)
			else:
				alast_start=alast_start+len(last)
				(aindex_begin,aindex_last,data)=asforlastandcompare(main_string,first,afirstStart,last,alast_start)
				return (aindex_begin,aindex_last,data)
		
		if (alast_start<afirstStart and afirstStart>(alast_start+len(last))):
			if (
				afirstStart-(alast_start+len(last)) <=3 and main_string[alast_start+len(last):afirstStart]!="," and main_string[alast_start+len(last):afirstStart]!="^-" and main_string[alast_start+len(last):afirstStart]!="-.->" and main_string[alast_start+len(last):afirstStart]!="^-.-"
				):	
				data="LF"
				return (alast_start,afirstStart,data)
			else:
				alast_start=alast_start+len(last)
				(aindex_begin,aindex_last,data)=asforlastandcompare(main_string,first,afirstStart,last,alast_start)
				return (aindex_begin,aindex_last,data)
			
	except ValueError:
		aindex_begin="0"
		aindex_last="0"
		data=""
		return (aindex_begin,aindex_last,data)		
		
		
def avar_link(arefVar,amParam,main_string):
	try:
		
		for amParam_count in range(len(amParam)):
			amParam_Relation=amParam[amParam_count]["relation"]
			amParam_Name=amParam[amParam_count]["name"]
			amParam_ClassName=amParam[amParam_count]["acName"]
			for aiList_Count in aiList:
				aiName=aiList_Count
				if aiName==amParam_Name:
					ae1="["+amParam_ClassName+"]"
					ae2="[<<interface>>;"+amParam_Name+"]"
					afirstStart=0
					alast_start=0
					data=""
					(afirstStart,alast_start,data)=asearch_first(main_string,ae1,afirstStart,ae2,alast_start)
					if (afirstStart=="0" and alast_start=="0" and data=="" ):
						main_string+=ae1+"uses -.->"+ae2+","
						break
					else:
						pass
						break
					
					
		for arefVar_count in range(len(arefVar)):
			arel1=arefVar[arefVar_count]["relation"]
			name=arefVar[arefVar_count]["name"]
			acName=arefVar[arefVar_count]["acName"]
			acount1 = 0
			aclassOrNot=0
			
			
			if arel1=="^-.-":
				main_string+="[<<interface>>;"+name+"]"+"^-.-"+"["+acName+"]"+","
			elif arel1=="-.->":
				main_string+="["+name+"]"+"-.->"+"[<<interface>>;"+acName+"]"+","
			elif arel1=="^-":
				main_string+="["+name+"]"+"^-"+"["+acName+"]"+","
			else:
				for aiList_Count in aiList:
					aiName=aiList_Count
					if aiName==name:
						acount1 = 1
						ae1="["+acName+"]"
						ae2="[<<interface>>;"+name+"]"
						afirstStart=0
						alast_start=0
						data=""
						(afirstStart,alast_start,data)=asearch_first(main_string,ae1,afirstStart,ae2,alast_start)
						if (data=="uses -.->"):
							main_string+=ae1+"-"+arel1+ae2+","
						elif (data=="FL"):
							main_string=main_string[:afirstStart+len(ae1)]+main_string[afirstStart+len(ae1):alast_start]+arel1+main_string[alast_start:]
						elif (data=="LF"):
							main_string=main_string[:afirstStart+len(ae2)]+arel1+main_string[afirstStart+len(ae2):alast_start]+main_string[alast_start:]
						
				
				if acount1 == 0:
					afirstStart=0
					alast_start=0
					data=""
					for acList_count in range(len(acList)):
						class_1=acList[acList_count]
						if name==class_1:
							aclassOrNot=1
					
					if aclassOrNot==1:
						ae1="["+acName+"]"
						ae2="["+name+"]"
						(afirstStart,alast_start,data)=asearch_first(main_string,ae1,afirstStart,ae2,alast_start)
						if (afirstStart=="0" and alast_start=="0" and data==""):
							main_string+=ae1+"-"+arel1+ae2+","
						elif (data=="FL"):
							main_string=main_string[:afirstStart+len(ae1)]+main_string[afirstStart+len(ae1):alast_start]+arel1+main_string[alast_start:]
						elif (data=="LF"):
							main_string=main_string[:afirstStart+len(ae2)]+arel1+main_string[afirstStart+len(ae2):alast_start]+main_string[alast_start:]
		return main_string		
	except ValueError:
		return main_string		
		
		
def agenImage(main_string):
	try:
		print main_string	
		r = requests.get('http://yuml.me/diagram/scruffy/class/%2F%2F Cool Class Diagram,' +main_string)
		print r.status_code
		if r.status_code == 200:
			urllib.urlretrieve ('http://yuml.me/diagram/scruffy/class/%2F%2F Cool Class Diagram,' +main_string, os.path.join(str(sys.argv[1]),str(sys.argv[2])+'.png'))
	except requests.ConnectionError:
		print("failed to connect with YUML")		
			

def aprocFile(aclass_interface,main_string):	
	try:
		
		main_string=type_declarations(aclass_interface,main_string)
		if str(type(aclass_interface))!="<class 'plyj.model.InterfaceDeclaration'>":
			abody_list=aclass_interface.body
			for abody_count in range(len(abody_list)):
				body=abody_list[abody_count]	
				avalidMeth = 1
				
				if str(type(body))=="<class 'plyj.model.ConstructorDeclaration'>":	
					main_string=aconst_Dec(body,main_string)
				global accessors
				accessors=aMod(body,accessors)
				if accessors == "+":		
					if str(type(body))=="<class 'plyj.model.MethodDeclaration'>" :
						global avList
						for avList_count in avList:
							if (
									"get"+avList_count.lower()== body.name.lower() or "asetter"+avList_count.lower()==body.name.lower()
								):
								avalidMeth = 0 
		
						if avalidMeth == 1:
							main_string=amethod(body,main_string)	
						
				#if (accessors == "+" or	accessors == "-"):
				if str(type(body))=="<class 'plyj.model.FieldDeclaration'>" :			
					main_string=adata_mem(body,main_string)
				accessors=""
		main_string+="]"+","
		avList = set()
		main_string=ainterImpl(aclass_interface,main_string)
		main_string=aext_Classes(aclass_interface,main_string)
		return main_string
	
	except ValueError:
		return main_string	

def aexContent(aclass_interface,main_string):
	try:
		main_string=type_declarations(aclass_interface,main_string)
		if str(type(aclass_interface))!="<class 'plyj.model.InterfaceDeclaration'>" :
			abody_list=aclass_interface.body
			for abody_count in range(len(abody_list)):
				body=abody_list[abody_count]	
				global accessors
				accessors=aMod(body,accessors)
				if accessors == "+":		
					if str(type(body))=="<class 'plyj.model.MethodDeclaration'>" :
						main_string=amethod(body,main_string)
				accessors=""		
		return main_string				
	except ValueError:
		return main_string			
		
	
for aFile in glob.glob("*.java"):
	ajhad=plyj.Parser().parse_file(aFile)

	atype_dec_list = ajhad.type_declarations
	for atype_dec_count in range(len(atype_dec_list)):
		acount_meth =0
		ac_var=0

		aclass_interface=atype_dec_list[atype_dec_count]
		main_string_1=aexContent(aclass_interface,main_string)
		main_string_1=""
	for atype_dec_count in range(len(atype_dec_list)):
		acount_meth =0
		aclass_interface=atype_dec_list[atype_dec_count]
		main_string=aprocFile(aclass_interface,main_string)
	am_name = set()	
main_string=avar_link(arefVar,amParam,main_string)		
agenImage(main_string)