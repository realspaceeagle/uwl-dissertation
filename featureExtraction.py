import pefile
import os
import csv
import array
import math

def cutit(s,n):
    return s[n:]

#The phrase File Entropy is used to measure the amount of data which is present in a selected file. For example, if you have some files and desire to calculate the entropy value for that, then it will be very simple by accessing the methods of File Entropy and its calculation process.
def get_entropy(data):
    if len(data) == 0:
        return 0.0
    occurences = array.array('L', [0] * 256)
    for x in data:
        occurences[x if isinstance(x, int) else ord(x)] += 1
    entropy = 0
    for x in occurences:
        if x:
            p_x = float(x) / len(data)
            entropy -= p_x * math.log(p_x, 2)
    return entropy


def get_resources(pe):
    """Extract resources :
    [entropy, size]"""
    resources = []
    print("Entropy.....#######################################")
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        try:
            for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                # print(resource_type)
                if hasattr(resource_type, 'directory'):
                    for resource_id in resource_type.directory.entries:
                        if hasattr(resource_id, 'directory'):
                            for resource_lang in resource_id.directory.entries:
                                data = pe.get_data(resource_lang.data.struct.OffsetToData,
                                                   resource_lang.data.struct.Size)
                                size = resource_lang.data.struct.Size
                                # print(resource_id)
                                entropy = get_entropy(data)
                                # print('Entropy........ ' + resource_type + '  ' + entropy + '  ' +size)
                                resources.append([entropy, size])
        except Exception as e:
            print("Entropy.....#############aaaaa##########################")
            return resources
    print("Entropy.....#######################################")
    return resources


def get_version_info(pe):
    """Return version infos"""
    print("Version Info.....#######################################")
    res = {}
    for fileinfo in pe.FileInfo:
        print(fileinfo)
        if fileinfo.keys == 'StringFileInfo':
            for st in fileinfo.StringTable:
                for entry in st.entries.items():
                    res[entry[0]] = entry[1]
        if fileinfo.Key == 'VarFileInfo':
            for var in fileinfo.Var:
                res[var.entry.items()[0][0]] = var.entry.items()[0][1]
    # print(pe)
    if hasattr(pe, 'VS_FIXEDFILEINFO'):
        print('llllllllll')
        res['flags'] = pe.VS_FIXEDFILEINFO.FileFlags
        res['os'] = pe.VS_FIXEDFILEINFO.FileOS
        res['type'] = pe.VS_FIXEDFILEINFO.FileType
        res['file_version'] = pe.VS_FIXEDFILEINFO.FileVersionLS
        res['product_version'] = pe.VS_FIXEDFILEINFO.ProductVersionLS
        res['signature'] = pe.VS_FIXEDFILEINFO.Signature
        res['struct_version'] = pe.VS_FIXEDFILEINFO.StrucVersion
    print("Version Info.....#####################aaaaa##################  ")
    print(res)
    print( "..#######################################")
    return res


def extract_infos(fpath):
    print("Infos.....#######################################")
    res = {}
    order = []
    pe = pefile.PE(fpath)
    res['Machine'] = pe.FILE_HEADER.Machine
    order.append('Machine')
    res['SizeOfOptionalHeader'] = pe.FILE_HEADER.SizeOfOptionalHeader
    order.append('SizeOfOptionalHeader')
    res['Characteristics'] = pe.FILE_HEADER.Characteristics
    order.append('Characteristics')
    res['MajorLinkerVersion'] = pe.OPTIONAL_HEADER.MajorLinkerVersion
    order.append('MajorLinkerVersion')
    res['MinorLinkerVersion'] = pe.OPTIONAL_HEADER.MinorLinkerVersion
    order.append('MinorLinkerVersion')
    res['SizeOfCode'] = pe.OPTIONAL_HEADER.SizeOfCode
    order.append('SizeOfCode')
    res['SizeOfInitializedData'] = pe.OPTIONAL_HEADER.SizeOfInitializedData
    order.append('SizeOfInitializedData')
    res['SizeOfUninitializedData'] = pe.OPTIONAL_HEADER.SizeOfUninitializedData
    order.append('SizeOfUninitializedData')
    res['AddressOfEntryPoint'] = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    order.append('AddressOfEntryPoint')
    res['BaseOfCode'] = pe.OPTIONAL_HEADER.BaseOfCode
    order.append('BaseOfCode')
    try:
        res['BaseOfData'] = pe.OPTIONAL_HEADER.BaseOfData
    except AttributeError:
        res['BaseOfData'] = 0
    order.append('BaseOfData')
    res['ImageBase'] = pe.OPTIONAL_HEADER.ImageBase
    order.append('ImageBase')
    res['SectionAlignment'] = pe.OPTIONAL_HEADER.SectionAlignment
    order.append('SectionAlignment')
    res['FileAlignment'] = pe.OPTIONAL_HEADER.FileAlignment
    order.append('FileAlignment')
    res['MajorOperatingSystemVersion'] = pe.OPTIONAL_HEADER.MajorOperatingSystemVersion
    order.append('MajorOperatingSystemVersion')
    res['MinorOperatingSystemVersion'] = pe.OPTIONAL_HEADER.MinorOperatingSystemVersion
    order.append('MinorOperatingSystemVersion')
    res['MajorImageVersion'] = pe.OPTIONAL_HEADER.MajorImageVersion
    order.append('MajorImageVersion')
    res['MinorImageVersion'] = pe.OPTIONAL_HEADER.MinorImageVersion
    order.append('MinorImageVersion')
    res['MajorSubsystemVersion'] = pe.OPTIONAL_HEADER.MajorSubsystemVersion
    order.append('MajorSubsystemVersion')
    res['MinorSubsystemVersion'] = pe.OPTIONAL_HEADER.MinorSubsystemVersion
    order.append('MinorSubsystemVersion')
    res['SizeOfImage'] = pe.OPTIONAL_HEADER.SizeOfImage
    order.append('SizeOfImage')
    res['SizeOfHeaders'] = pe.OPTIONAL_HEADER.SizeOfHeaders
    order.append('SizeOfHeaders')
    res['CheckSum'] = pe.OPTIONAL_HEADER.CheckSum
    order.append('CheckSum')
    res['Subsystem'] = pe.OPTIONAL_HEADER.Subsystem
    order.append('Subsystem')
    res['DllCharacteristics'] = pe.OPTIONAL_HEADER.DllCharacteristics
    order.append('DllCharacteristics')
    res['SizeOfStackReserve'] = pe.OPTIONAL_HEADER.SizeOfStackReserve
    order.append('SizeOfStackReserve')
    res['SizeOfStackCommit'] = pe.OPTIONAL_HEADER.SizeOfStackCommit
    order.append('SizeOfStackCommit')
    res['SizeOfHeapReserve'] = pe.OPTIONAL_HEADER.SizeOfHeapReserve
    order.append('SizeOfHeapReserve')
    res['SizeOfHeapCommit'] = pe.OPTIONAL_HEADER.SizeOfHeapCommit
    order.append('SizeOfHeapCommit')
    res['LoaderFlags'] = pe.OPTIONAL_HEADER.LoaderFlags
    order.append('LoaderFlags')
    res['NumberOfRvaAndSizes'] = pe.OPTIONAL_HEADER.NumberOfRvaAndSizes
    order.append('NumberOfRvaAndSizes')

    # Sections
    res['SectionsNb'] = len(pe.sections)
    order.append('SectionsNb')
    entropy = map(lambda x: x.get_entropy(), pe.sections)
    res['SectionsMeanEntropy'] = sum(entropy) / float(len(entropy))
    order.append('SectionsMeanEntropy')
    res['SectionsMinEntropy'] = min(entropy)
    order.append('SectionsMinEntropy')
    res['SectionsMaxEntropy'] = max(entropy)
    order.append('SectionsMaxEntropy')
    raw_sizes = map(lambda x: x.SizeOfRawData, pe.sections)
    res['SectionsMeanRawsize'] = sum(raw_sizes) / float(len(raw_sizes))
    order.append('SectionsMeanRawsize')
    res['SectionsMinRawsize'] = min(raw_sizes)
    order.append('SectionsMinRawsize')
    res['SectionMaxRawsize'] = max(raw_sizes)
    order.append('SectionMaxRawsize')
    virtual_sizes = map(lambda x: x.Misc_VirtualSize, pe.sections)
    res['SectionsMeanVirtualsize'] = sum(virtual_sizes) / float(len(virtual_sizes))
    order.append('SectionsMeanVirtualsize')
    res['SectionsMinVirtualsize'] = min(virtual_sizes)
    order.append('SectionsMinVirtualsize')
    res['SectionMaxVirtualsize'] = max(virtual_sizes)
    order.append('SectionMaxVirtualsize')

    # Imports
    try:
        res['ImportsNbDLL'] = len(pe.DIRECTORY_ENTRY_IMPORT)
        imports = sum([x.imports for x in pe.DIRECTORY_ENTRY_IMPORT], [])
        res['ImportsNb'] = len(imports)
        res['ImportsNbOrdinal'] = len(filter(lambda x: x.name is None, imports))
    except AttributeError:
        res['ImportsNbDLL'] = 0
        res['ImportsNb'] = 0
        res['ImportsNbOrdinal'] = 0
    order.append('ImportsNbDLL')
    order.append('ImportsNb')
    order.append('ImportsNbOrdinal')
    # Exports
    try:
        res['ExportNb'] = len(pe.DIRECTORY_ENTRY_EXPORT.symbols)
    except AttributeError:
        # No export
        res['ExportNb'] = 0
    order.append('ExportNb')
    # Resources
    resources = get_resources(pe)
    res['ResourcesNb'] = len(resources)
    order.append('ResourcesNb')
    if len(resources) > 0:
        entropy = map(lambda x: x[0], resources)
        res['ResourcesMeanEntropy'] = sum(entropy) / float(len(entropy))
        res['ResourcesMinEntropy'] = min(entropy)
        res['ResourcesMaxEntropy'] = max(entropy)
        sizes = map(lambda x: x[1], resources)
        res['ResourcesMeanSize'] = sum(sizes) / float(len(sizes))
        res['ResourcesMinSize'] = min(sizes)
        res['ResourcesMaxSize'] = max(sizes)
    else:
        res['ResourcesNb'] = 0
        res['ResourcesMeanEntropy'] = 0
        res['ResourcesMinEntropy'] = 0
        res['ResourcesMaxEntropy'] = 0
        res['ResourcesMeanSize'] = 0
        res['ResourcesMinSize'] = 0
        res['ResourcesMaxSize'] = 0
    order.append('ResourcesMeanEntropy')
    order.append('ResourcesMinEntropy')
    order.append('ResourcesMaxEntropy')
    order.append('ResourcesMeanSize')
    order.append('ResourcesMinSize')
    order.append('ResourcesMaxSize')
    # Load configuration size
    try:
        res['LoadConfigurationSize'] = pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.Size
    except AttributeError:
        res['LoadConfigurationSize'] = 0
    order.append('LoadConfigurationSize')
    # Version configuration size
    try:
        version_infos = get_version_info(pe)
        print('asasasasas')
        print(version_infos)
        res['VersionInformationSize'] = len(version_infos.keys())
    except AttributeError:
        res['VersionInformationSize'] = 0
    order.append('VersionInformationSize')
    # print("Infos.....#######################################  ")
    # for i in res:
    #     print(i + ' : ' + str(res[i]))
    # print("..#######################################")
    return order,res
