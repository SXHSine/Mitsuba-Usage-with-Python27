# -*- coding: UTF-8 -*-
import os
import sys
# NOTE: remember to specify paths using FORWARD slashes (i.e. '/' instead of
# '\' to avoid pitfalls with string escaping)
# Configure the search path for the Python extension module
sys.path.append('D:/ProgramFiles/Mitsuba 0.5.0/python/2.7')
# Ensure that Python will be able to find the Mitsuba core libraries
os.environ['PATH'] = 'path-to-mitsuba-directory' + \
    os.pathsep + os.environ['PATH']

import mitsuba
from mitsuba.core import *
from mitsuba.render import SceneHandler

from xml.etree.ElementTree import ElementTree, Element


def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    '''将xml文件写出
       tree: xml树
       out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def getTheShape(filename):
    for s in root.findall('shape'):
        for pro in s:
            if pro.tag == "string" and pro.attrib["value"] == filename:
                return s
    return None


def setTranslate(shape, Point):
    if shape == None:
        print "None such filename"
        return
    trans = shape.findall("transform/translate")[0]
    shape.findall("transform/translate")[0].attrib['x'] = str(float(Point[0]))
    shape.findall("transform/translate")[0].attrib['y'] = str(float(Point[1]))
    shape.findall("transform/translate")[0].attrib['z'] = str(float(Point[2]))


def setLookat(camera, point_origin, point_target):
    list_point_origin, list_point_target = [point_origin[0], point_origin[
        1], point_origin[2]], [point_target[0], point_target[1], point_target[2]]
    list_point_origin, list_point_target = [str(x) for x in list_point_origin], [
        str(x) for x in list_point_target]
    if camera == None:
        print "None such typename"
        return
    lookat = camera.findall("transform/lookat")[0]
    lookat.attrib['origin'] = ','.join(list_point_origin)
    lookat.attrib['target'] = ','.join(list_point_target)


def changeXML_translate(path_xml, filename, Point):
    tree = read_xml(path_xml)
    root = tree.getroot()
    shape = None
    for s in root.findall('shape'):
        for pro in s:
            if pro.tag == "string" and pro.attrib["value"] == filename:
                shape = s
    setTranslate(shape, Point)
    write_xml(tree, path_xml)


def changeXML_lookat(path_xml, typename, point_origin, point_target):
    tree = read_xml(path_xml)
    root = tree.getroot()
    camera = None
    for s in root.findall('sensor'):
        if s.attrib['type'] == typename:
            camera = s
    setLookat(camera, point_origin, point_target)
    write_xml(tree, path_xml)


##USAGE##
# changeXML_translate("scene_objs _test.xml", "cow.obj",  Point(0,0,0))


if __name__ == '__main__':
    tree = read_xml("xxx.xml")
    root = tree.getroot()
    for s in root.findall('shape'):
        print s.findall('transform/translate')[0].attrib

    shape = getTheShape("cow.obj")
    setTranslate(shape, Point(0, 0, 0))
    print shape.findall('transform/translate')[0].attrib
    for s in root.findall('shape'):
        print s.findall('transform/translate')[0].attrib

    write_xml(tree, "xxx.xml")
