#!/usr/bin/env python3.8
from listener import LabellingNode
import glob, os, time
import subprocess
import threading, multiprocessing
import psutil
import rospy
import sys
import re
import random 
def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def replace_object(file_name, line_num, object_name):
    lines = open(file_name, 'r').readlines()
    text = '\t \t \t \t \t \t \t \t \t<uri>chimneys/%s</uri>  \n' % object_name
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def replace_scale(file_name, line_num, scale):
    lines = open(file_name, 'r').readlines()
    text = '\t \t \t \t \t \t \t \t \t<scale>%f %f %f</scale>  \n' % scale
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


def random_scaling(sequence_no):
    '''
    z: between 0.1 and 0.5
    x,y: between 0.07 and 0.4
    '''
    if sequence_no < 20:
        return (0.1,0.1,0.2)
    elif sequence_no >= 20 and sequence_no < 40:
        x = random.uniform(0.07,0.4)
        z = random.uniform(0.07,0.4)
        return (x,x,z)
    elif sequence_no >= 40 and sequence_no < 60:
        x = random.uniform(0.1,0.4)
        y = random.uniform(0.1,0.4)
        z = random.uniform(0.1,0.5)
        return (x,y,z)
    else:
        return (0.1,0.1,0.2)

if __name__ == '__main__':
    sequence_incrementer = 0
    cwd = os.getcwd()
    #print(os.path.join(cwd, "/chimneys"))
    os.chdir(cwd + '/chimneys')
    files = glob.glob('*.STL')
    obs =  sorted(files, key=lambda x:float(re.findall("(\d+)",x)[0]))
    for obj in obs:
        time.sleep(10) # cooldown pause between runs
        print("RUN number %d \n \n" %  sequence_incrementer)
        # Folder creations
        sequence_path = cwd + '/chimney_dataset/' + str(sequence_incrementer)
        sequence_ouster_path = os.path.join(sequence_path, 'velodyne')
        sequence_label_path = os.path.join(sequence_path, 'labels')

        # make txt with filename etcs
        try:
            os.mkdir(sequence_path)
            os.mkdir(sequence_ouster_path)
            os.mkdir(sequence_label_path)
        except FileNotFoundError:
            print("Directory: {0} does not exist".format(sequence_path))
        except NotADirectoryError:
            print("{0} is not a directory".format(sequence_path))
        except PermissionError:
            print("You do not have permissions to change to {0}".format(sequence_path))
        except FileExistsError:
            pass

        # Main processing line
        scale = random_scaling(sequence_incrementer)
        f= open(sequence_path + "/meta.txt","w+")
        f.write("RUN %d with object %s" % (sequence_incrementer,obj))
        f.write(" and scaling %f %f %f" % scale)
        f.close()
        replace_scale('/home/marius/Development/SemanticSegmentation/segment.sdf',1301,scale)
        replace_object('/home/marius/Development/SemanticSegmentation/segment.sdf',1302,obj)
        proc = subprocess.Popen(['roslaunch', '/home/marius/Development/SemanticSegmentation/launch/segmentation.launch', 'directory:=' + sequence_path])
        time.sleep(5)
        proc2 = subprocess.Popen(['/home/marius/Development/SemanticSegmentation/build/creator'])

        while not rospy.is_shutdown():
            try:
                proc.wait(timeout=1800)
            except subprocess.TimeoutExpired:
                try:
                    kill(proc.pid)
                    kill(proc2.pid)
                    del proc2
                    del proc
                    break
                except psutil.NoSuchProcess:
                    break
            except Exception as e:
                print(e)
                break
        print("FINISHING RUN")
        sequence_incrementer += 1
    for obj in obs:
        if sequence_incrementer > 0:
            time.sleep(10) # cooldown pause between runs
            print("RUN number %d \n \n" %  sequence_incrementer)
            # Folder creations
            sequence_path = cwd + '/chimney_dataset/' + str(sequence_incrementer)
            sequence_ouster_path = os.path.join(sequence_path, 'velodyne')
            sequence_label_path = os.path.join(sequence_path, 'labels')

            # make txt with filename etcs
            try:
                os.mkdir(sequence_path)
                os.mkdir(sequence_ouster_path)
                os.mkdir(sequence_label_path)
            except FileNotFoundError:
                print("Directory: {0} does not exist".format(sequence_path))
            except NotADirectoryError:
                print("{0} is not a directory".format(sequence_path))
            except PermissionError:
                print("You do not have permissions to change to {0}".format(sequence_path))
            except FileExistsError:
                pass

            # Main processing line
            scale = random_scaling(sequence_incrementer)
            f= open(sequence_path + "/meta.txt","w+")
            f.write("RUN %d with object %s" % (sequence_incrementer,obj))
            f.write("and scaling %f %f %f" % scale)
            f.close()
            replace_scale('/home/marius/Development/SemanticSegmentation/segment.sdf',1301,scale)
            replace_object('/home/marius/Development/SemanticSegmentation/segment.sdf',1302,obj)
            proc = subprocess.Popen(['roslaunch', '/home/marius/Development/SemanticSegmentation/launch/segmentation.launch', 'directory:=' + sequence_path])
            time.sleep(5)
            proc2 = subprocess.Popen(['/home/marius/Development/SemanticSegmentation/build/creator'])
            while not rospy.is_shutdown():
                try:
                    proc.wait(timeout=1800)
                except subprocess.TimeoutExpired:
                    try:
                        kill(proc.pid)
                        kill(proc2.pid)
                        del proc2
                        del proc
                        break
                    except psutil.NoSuchProcess:
                        break
                except Exception as e:
                    print(e)
                    break

            print("FINISHING RUN")
            sequence_incrementer += 1
        else:
            print(sequence_incrementer)
            sequence_incrementer +=1

    for obj in obs:
        time.sleep(10) # cooldown pause between runs
        print("RUN number %d \n \n" %  sequence_incrementer)
        # Folder creations
        sequence_path = cwd + '/chimney_dataset/' + str(120 + sequence_incrementer)
        sequence_ouster_path = os.path.join(sequence_path, 'velodyne')
        sequence_label_path = os.path.join(sequence_path, 'labels')

        # make txt with filename etcs
        try:
            os.mkdir(sequence_path)
            os.mkdir(sequence_ouster_path)
            os.mkdir(sequence_label_path)
        except FileNotFoundError:
            print("Directory: {0} does not exist".format(sequence_path))
        except NotADirectoryError:
            print("{0} is not a directory".format(sequence_path))
        except PermissionError:
            print("You do not have permissions to change to {0}".format(sequence_path))
        except FileExistsError:
            pass

        # Main processing line
        scale = random_scaling(sequence_incrementer)
        f= open(sequence_path + "/meta.txt","w+")
        f.write("RUN %d with object %s" % (sequence_incrementer,obj))
        f.write("and scaling %f %f %f" % scale)
        f.close()
        replace_scale('/home/marius/Development/SemanticSegmentation/segment.sdf',1301,scale)
        replace_object('/home/marius/Development/SemanticSegmentation/segment.sdf',1302,obj)
        proc = subprocess.Popen(['roslaunch', '/home/marius/Development/SemanticSegmentation/launch/segmentation.launch', 'directory:=' + sequence_path])
        time.sleep(5)
        proc2 = subprocess.Popen(['/home/marius/Development/SemanticSegmentation/build/creator'])

        while not rospy.is_shutdown():
            try:
                proc.wait(timeout=1800)
            except subprocess.TimeoutExpired:
                try:
                    kill(proc.pid)
                    kill(proc2.pid)
                    del proc2
                    del proc
                    break
                except psutil.NoSuchProcess:
                    break
            except Exception as e:
                print(e)
                break

        sequence_incrementer += 1

