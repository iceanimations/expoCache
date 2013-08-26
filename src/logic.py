import os
import re
import subprocess
import os.path as osp
import site
site.addsitedir(r'R:\Pipe_Repo\Users\Qurban\mayaize')
import mayaize2011
import mayaize2012
import mayaize2013
import pymel.core as pc


def openScene(path):
    '''
    opens a maya scene in mayapy
    '''
    pc.openFile(path, f = True)

def objects(typ):
    '''
    returns the objects of the specified type from the opened maya scene
    '''
    defaultSets = ['defaultLightSet', 'defaultObjectSet',
                   'front', 'top', 'side', 'persp']
    objectSets = []
    objects = pc.ls(type = typ)
    if typ == 'camera':
        for obj in objects:
            obj = str(obj.getParent())
            if obj not in defaultSets:
                objectSets.append(str(obj))
    else:
        for obj in objects:
            try:
                if type(obj) == pc.nt.ObjectSet and str(obj) not in defaultSets:
                    transform = obj.members()[0]
                    if type(transform) == pc.nt.Transform:
                        shape = transform.getShape()
                        if type(shape) == pc.nt.Mesh:
                            obj = str(obj)
                            objectSets.append(obj)
            except IndexError:
                pass
            except pc.general.MayaAttributeError:
                pass
            
    return objectSets

def setCurrentUnit(fps, kkacf):
    pc.general.currentUnit(time = fps, ua = not kkacf)

def gotoPath(path):
    '''
    opens the window explorer where the caches are exported
    '''
    if path and osp.exists(path):
        subprocess.Popen('explorer /select,'+ osp.normpath(path))

def combineSet(_sets = []):
    '''
    combines a maya set and retruns a combined mesh
    '''
    combineMeshes = []
    for objectSet in [pc.PyNode(_set) for _set in _sets]:
        pc.select(objectSet.members())
        meshes = [shape for transform in objectSet.dsm.inputs(type = "transform") for shape in transform.getShapes(type = "mesh", ni = True)]
        combineMesh = pc.createNode("mesh")
        pc.rename(combineMesh, objectSet.split(":")[-1]+"_cache")
        combineMeshes.append(combineMesh)
        polyUnite = pc.createNode("polyUnite")
        for i in xrange(0, len(meshes)):
            meshes[i].outMesh >> polyUnite.inputPoly[i]
            meshes[i].worldMatrix[0] >> polyUnite.inputMat[i]
        polyUnite.output >> combineMesh.inMesh
    return combineMeshes

def removeCombinedMeshes(meshes = []):
    '''
    removes the combined meshes from the scene
    '''
    pc.delete(map(lambda x: x.getParent(), meshes))

def export(path, settings):
    '''
    exports the cache of the specified mesh at the specified path
    according to the provided settings
    '''
    # construct the arguments dictionary for the export command
    flags = {"version": 5,
             "time_range_mode": settings['time_range_mode'],
             "start_time": settings['start_time'],
             "end_time": settings['end_time'],
             "cache_file_dist": "OneFile",
             "refresh_during_caching": 0,
             "cache_dir": settings['cache_dir'],
             "cache_per_geo": "1",
             "cache_name": "",
             "cache_name_as_prefix": 0,
             "action_to_perform": "export",
             "force_save": 0,
             "simulation_rate": 1,
             "sample_multiplier": 1,
             "inherit_modf_from_cacha": 1,
             "store_doubles_as_float":1,
             "cache_format": "mcc"}
    # construct the export command
    command =  '''doCreateGeometryCache2 {version} {{ "{time_range_mode}",
                "{start_time}", "{end_time}", "{cache_file_dist}",
                "{refresh_during_caching}", "{cache_dir}", "{cache_per_geo}",
                "{cache_name}", "{cache_name_as_prefix}", "{action_to_perform}",
                "{force_save}", "{simulation_rate}", "{sample_multiplier}",
                "{inherit_modf_from_cacha}", "{store_doubles_as_float}",
                "{cache_format}"}};'''.format(**flags)
    # evaluate the command
    pc.Mel.eval(command)

def select(objects = []):
    '''
    selects the specified objects in the opened maya scene
    '''
    objs = []
    for obj in objects:
        objs.append(pc.PyNode(obj))
    pc.select(objs)

def exportSelection(path):
    '''
    exports the selection from opened maya scene to the
    specified path
    '''
    pc.exportSelected(path,
                      force=True,
                      expressions = True,
                      constructionHistory = True,
                      channels = True,
                      shader = True,
                      constraints = True,
                      options="v=0",
                      typ="mayaAscii",
                      pr = True)

def purgeChar(string, pattern = r"\W", replace = ""):
        return re.sub(r"[%s]" %pattern, replace, str(string))

def normPath(path):
    return osp.normpath(path)

def dirname(path):
    return osp.dirname(path)

def exists(path):
    return osp.exists(path)

def join(path1, path2):
    return osp.join(path1, path2)

def pyNode(name):
    return pc.PyNode(name)


def doCreateGeometryCache2():
    doCreateGeometryCache2 =r'''global proc string[] doCreateGeometryCache2 ( int $version, string $args[] )
    //A facsimle copy of doCreateGeometryCache just that args[6] i.e. export cache
    //per geometry is fixed to 1 regardless of group caching
    {
        string $cacheFiles[];
        if(( $version > 5 ) || ( size($args) > 16 )) {
                error( (uiRes("m_doCreateGeometryCache.kBadArgsError")));
                return $cacheFiles;
        }

        string  $cacheDirectory         = "";
        string  $fileName                       = "";
        int             $useAsPrefix            = 0;
        int             $perGeometry            = 0;
        string  $action        = "replace";
        int     $force = 0;
        int             $inherit = 0;
        int     $doubleToFloat = 0;
        string $distribution = "OneFilePerFrame";

        int     $rangeMode                      = $args[0];
        float   $diskCacheStartTime = $args[1];
        float   $diskCacheEndTime   = $args[2];
        float   $simulationRate         = 1.0;
        int             $sampleMultiplier       = 1;

        float  $startTime = $diskCacheStartTime;
        float  $endTime = $diskCacheEndTime;
        string $format = "mcc";         // Maya's default internal format

        if( $rangeMode == 1 ) {
        $startTime = `getAttr defaultRenderGlobals.startFrame`;
        $endTime = `getAttr defaultRenderGlobals.endFrame`;
        } else if( $rangeMode == 2 ) {
                $startTime = `playbackOptions -q -min`;
                $endTime = `playbackOptions -q -max`;
        }

        if ($version > 1) {
            $distribution = $args[3];
                $cacheDirectory = $args[5];
                $perGeometry = $args[6];
                $fileName = $args[7];
                $useAsPrefix = $args[8];
        }
        if ($version > 2) {
                $action = $args[9];
                $force = $args[10];

                if( size($args) > 11 ) {
                        $simulationRate = $args[11];
                }
                if( size($args) > 12 ) {
                        $sampleMultiplier = $args[12];
                }
                else {
                        $sampleMultiplier = 1;
                }
        }
        if( $version > 3 ) {
                $inherit = $args[13];
                $doubleToFloat = $args[14];
        }

        if( $version > 4 ) {
                $format = $args[15];
        }

        // Call doMergeCache instead since it handles gaps between
        // caches correctly.
        if( $action == "merge" || $action == "mergeDelete" )
        {

                string $mergeArgs[];
                $mergeArgs[0] = 1;
                $mergeArgs[1] = $startTime;
                $mergeArgs[2] = $endTime;
                $mergeArgs[3] = $args[3];
                $mergeArgs[4] = $cacheDirectory;
                $mergeArgs[5] = $fileName;
                $mergeArgs[6] = $useAsPrefix;
                $mergeArgs[7] = $force;
                $mergeArgs[8] = $simulationRate;
                $mergeArgs[9] = $sampleMultiplier;
                $mergeArgs[10] = $action;
                $mergeArgs[11] = "geom";
                $mergeArgs[12] = $format;
                return doMergeCache(2, $mergeArgs);
        }

        // If we're replacing a cache, and inheriting modifications,
        // the new cache should have the same translation, scaling
        // and clipping as the original. So store these values and
        // set after cache creation.
        //
        float $startFrame[] = {};
        float $sourceStart[] = {};
        float $sourceEnd[] = {};
        float $scale[] = {};

        select -d `ls -sl -type cacheFile`;
        string $objsToCache[] = getGeometriesToCache();
        if (size($objsToCache) == 0) {
                error((uiRes("m_doCreateGeometryCache.kMustSelectGeom")));
        } else  if ($action == "replace") {
                if (!getCacheCanBeReplaced($objsToCache)) {
                        return $cacheFiles;
                }

                if( $inherit ) {
                        string $obj, $cache;
                        for( $obj in $objsToCache ) {
                                string $existing[] = findExistingCaches($obj);
                                int $index = size($startFrame);
                                $startFrame[$index] = `getAttr ($existing[0]+".startFrame")`;
                                $sourceStart[$index] = `getAttr ($existing[0]+".sourceStart")`;
                                $sourceEnd[$index] = `getAttr ($existing[0]+".sourceEnd")`;
                                $scale[$index] = `getAttr ($existing[0]+".scale")`;
                        }
                }
        }

        // If the user has existing cache groups on some of the geometry,
        // then they cannot attach new caches per geometry.
        //
    string $cacheGroups[] = `getObjectsByCacheGroup($objsToCache)`;
        if (size($cacheGroups) != size($objsToCache)) {
                $perGeometry = 1;
                $args[6] = 1; // used below in generating cache file command
                //warning( (uiRes("m_doCreateGeometryCache.kIgnoringPerGeometry")) );
        }

        // Check if directory has caches that might be overwritten
        //
        string $cacheDirectory = getCacheDirectory(     $cacheDirectory,
                                                                                                $objsToCache, $fileName,
                                                                                                $useAsPrefix, $perGeometry,
                                                                                                $action, $force, 1);

        if ($cacheDirectory == "") {
                return $cacheFiles;
        }
        else if ($cacheDirectory == "rename") {
                performCreateGeometryCache 1 $action;
                error((uiRes("m_doCreateGeometryCache.kNameAlreadyInUse")));
                return $cacheFiles;
        }

        // if we're replacing, delete active caches.
        //
        if( $action == "replace" ) {
                for( $obj in $objsToCache ) {
                        string $all[] = findExistingCaches($obj);
                        for( $cache in $all) {
                                if( `getAttr ($cache+".enable")`) {
                                        deleteCacheFile(2, {"keep",$cache});
                                }
                        }
                }
        }

        // create the cache(s)
        //
        if ($action == "add" || $action == "replace") {
                setCacheEnable(0, 1, $objsToCache);
        }

        // generate the cacheFile command to write the caches
        //
        string $cacheCmd = getCacheFileCmd($version, $cacheDirectory, $args);
        int $ii = 0;

        //segmented cache files are employed in the case of one large cache file that
        //exceeds 2GB in size.  Since we currently cannot handle such large files, we will
        //automatically generate several caches, each less than 2GB.
        int $useSegmentedCacheFile = 0;
        int $numSegments = 0;
        if($distribution == "OneFile" && !$perGeometry) {
            string $queryCacheSizeCmd = "cacheFile";
            for ($ii = 0; $ii < size($objsToCache); $ii++) {
                    $queryCacheSizeCmd += (" -points "+$objsToCache[$ii]);
            }
            $queryCacheSizeCmd += " -q -dataSize";
            if($doubleToFloat) {
                $queryCacheSizeCmd += " -dtf";
            }
            float $dataSizePerFrame = `eval $queryCacheSizeCmd`;
            float $maxSize = 2147000000; //approximate size of max signed int.
            float $numSamples = ($endTime - $startTime + 1.0)/($simulationRate*$sampleMultiplier);
            float $dataSize = $dataSizePerFrame*$numSamples;
            if($dataSize > $maxSize) {
                $useSegmentedCacheFile = 1;
                $numSegments = floor($dataSize / $maxSize) + 1;
            }
        }

        if(!$useSegmentedCacheFile) {
            if( $fileName != "" ) {
                    $cacheCmd += ("-fileName \"" + $fileName + "\" ");
            }
            $cacheCmd += ("-st "+$startTime+" -et "+$endTime);
            for ($ii = 0; $ii < size($objsToCache); $ii++) {
                    $cacheCmd += (" -points "+$objsToCache[$ii]);
            }
            $cacheFiles = `eval $cacheCmd`;
        }
        else {
            int $jj;
            float $segmentStartTime = $startTime;
            float $segmentEndTime;
            float $segmentLength = ($endTime - $startTime)/$numSegments;
            string $segmentCacheCmd ;
            string $segmentCacheName = "";
            string $segmentCacheFiles[];
            for($jj = 0; $jj< $numSegments; $jj++) {
                $segmentCacheCmd = $cacheCmd;
                if($fileName != "")
                    $segmentCacheName = $fileName;
                else
                    $segmentCacheName = getAutomaticCacheName();
                $segmentEndTime = $segmentStartTime + floor($segmentLength);

                $segmentCacheName += ("Segment" + ($jj+1));
                $segmentCacheCmd += (" -fileName \"" + $segmentCacheName + "\" ");

                $segmentCacheCmd += ("-st "+$segmentStartTime+" -et "+$segmentEndTime);
                for ($ii = 0; $ii < size($objsToCache); $ii++) {
                        $segmentCacheCmd += (" -points "+$objsToCache[$ii]);
                }
                $segmentCacheFiles = `eval $segmentCacheCmd`;
                $segmentStartTime = $segmentEndTime + 1;

                $cacheFiles[size($cacheFiles)] = $segmentCacheFiles[0];
            }
    }

        if ($action == "export") {
                for ($ii = 0; $ii < size($cacheFiles); $ii++) {
                        $cacheFiles[$ii] = ($cacheDirectory+"/"+$cacheFiles[$ii]+".xml");
                }
                // In export mode, we do not want to attach the cache. We are done.
                //
                return $cacheFiles;
        }


        // attach the caches to the history switch
        //
        if($useSegmentedCacheFile) {
            if(size($objsToCache) == 1) {
                for($ii=0;$ii<size($cacheFiles);$ii++) {
                    string $segmentCacheFile[];
                    $segmentCacheFile[0] = $cacheFiles[$ii];
                    attachOneCachePerGeometry(  $segmentCacheFile, $objsToCache,
                                                                        $cacheDirectory, $action, $format );
                }
            }
            else {
                for($ii=0;$ii<size($cacheFiles);$ii++) {
                    string $segmentCacheFile[];
                    $segmentCacheFile[0] = $cacheFiles[$ii];
                    attachCacheGroups( $segmentCacheFile,$objsToCache,$cacheDirectory,$action, $format );
                }
            }

        }
        else if( $perGeometry || size($objsToCache) == 1) {
                attachOneCachePerGeometry(      $cacheFiles, $objsToCache,
                                                                        $cacheDirectory, $action, $format );
        } else {
                if( size($cacheFiles) != 1 ) {
                        error( (uiRes("m_doCreateGeometryCache.kInvalidCacheOptions")));
                }

                attachCacheGroups( $cacheFiles,$objsToCache,$cacheDirectory,$action, $format );

        }

        // If we're replacing a cache and inheriting modifications,
        // restore the translation, scaling, clipping etc.
        if( $action == "replace" && $inherit )
        {
                int $i = 0;
                for( $i = 0; $i < size($objsToCache); $i++)
                {
                        string $cache[] = findExistingCaches($objsToCache[$i]);
                        float $sStart = `getAttr ($cache[0]+".sourceStart")`;
                        float $sEnd = `getAttr ($cache[0]+".sourceEnd")`;

                        if( $sStart != $sourceStart[$i] &&
                                $sourceStart[$i] >= $sStart &&
                                $sourceStart[$i] <= $sEnd )
                        {
                                cacheClipTrimBefore( $cache[0], $sourceStart[$i] );
                        }

                        if( $sEnd != $sourceEnd[$i] &&
                                $sourceEnd[$i] >= $sStart &&
                                $sourceEnd[$i] <= $sEnd )
                        {
                                cacheClipTrimAfter( $cache[0], $sourceEnd[$i] );
                        }

                        setAttr ($cache[0] + ".startFrame") $startFrame[$i];
                        setAttr ($cache[0] + ".scale") $scale[$i];
                }
        }
        select -r $objsToCache;
        return $cacheFiles;
    };'''

    pc.Mel.eval(doCreateGeometryCache2)
