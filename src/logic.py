import os
import os.path as osp
import pymel.core as pc


def openScene(path):
    '''
    opens a maya scene in mayapy
    '''
    pass

def objects(typ):
    '''
    returns the objects of the specified type from the opened maya scene
    '''
    pass

def gotoPath(path):
    '''
    opens the window explorer where the caches are exported
    '''
    pass

def combineSet(_set):
    '''
    combines a maya set and retruns a combined mesh
    '''
    pass

def export(mesh, path, settings):
    '''
    exports the cache of the specified mesh at the specified path
    according to the provided settings
    '''
    pass

def select(objects = []):
    '''
    selects the specified objects in the opened maya scene
    '''
    pass

def exportSelection(path):
    '''
    exports the selection from opened maya scene to the
    specified path
    '''
    pass