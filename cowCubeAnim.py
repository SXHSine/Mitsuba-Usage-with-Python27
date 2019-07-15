import os
import sys
sys.path.append('D:/ProgramFiles/Mitsuba 0.5.0/python/2.7')
os.environ['PATH'] = 'path-to-mitsuba-directory' + \
    os.pathsep + os.environ['PATH']
import mitsuba
from mitsuba.core import *
from mitsuba.render import SceneHandler
from mitsuba.render import RenderQueue, RenderJob
import multiprocessing
# deal with XML to transform shape
import processXML
import animation


# Positons
# step 0
# camera_for: y_ori+0.8
camera_oriPos, camera_oriFor = Point(-0.435,
                                     1.000, -4.438), Point(0.050, 0.8, 0.997)
camera_lookLeft_pos, camera_lookLeft_for = Point(
    -0.972, 0.896, -1.922), Point(0.517, 0.8, 0.854)
camera_lookRight_pos, camera_lookRight_for = Point(
    1.434, 0.883, -1.327), Point(-0.627, 0.7, 1.0)

# step 1
camera_lookCow_pos_1, camera_lookCow_for_1 = Point(
    -0.234, 0.774, 5.0), Point(3.5, 0.8, 2.0)
camera_lookCow_pos_2, camera_lookCow_for_2 = Point(
    -0.234, 0.774, 5.0), Point(3.5, 0.0, 2.0)
camera_lookCowLeft_pos_1, camera_lookCowLeft_for_1 = Point(
    0.5, 0.772, 4.0), Point(2.0, 0.8, 2.0)
camera_lookCowLeft_pos_2, camera_lookCowLeft_for_2 = Point(
    0.5, 0.772, 4.0), Point(2.0, 0.0, 2.0)

cow_oriPos, cow_newPos = Point(1.5, -1, 2.5), Point(1.5, -1, 1.5)

bal = animation.BasicAnimList()
# total 1050
# step 0    390
ba = animation.BasicAnim(animation.BasicPos(camera_oriPos, camera_oriFor),
                         animation.BasicPos(camera_oriPos, camera_oriFor), 30)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_oriPos, camera_oriFor),
                         animation.BasicPos(camera_lookLeft_pos, camera_lookLeft_for), 60)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookLeft_pos, camera_lookLeft_for),
                         animation.BasicPos(camera_lookLeft_pos, camera_lookLeft_for), 30)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookLeft_pos, camera_lookLeft_for),
                         animation.BasicPos(camera_oriPos, camera_oriFor), 60)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_oriPos, camera_oriFor),
                         animation.BasicPos(camera_oriPos, camera_oriFor), 30)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_oriPos, camera_oriFor),
                         animation.BasicPos(camera_lookRight_pos, camera_lookRight_for), 60)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookRight_pos, camera_lookRight_for),
                         animation.BasicPos(camera_lookRight_pos, camera_lookRight_for), 30)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookRight_pos, camera_lookRight_for),
                         animation.BasicPos(camera_oriPos, camera_oriFor), 60)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_oriPos, camera_oriFor),
                         animation.BasicPos(camera_oriPos, camera_oriFor), 30)
bal.addAnimation("camera", ba)

# step 1 210+120+210+120 = 660
ba = animation.BasicAnim(animation.BasicPos(camera_oriPos, camera_oriFor),
                         animation.BasicPos(camera_lookCow_pos_1, camera_lookCow_for_1), 90)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookCow_pos_1, camera_lookCow_for_1),
                         animation.BasicPos(camera_lookCow_pos_2, camera_lookCow_for_2), 90)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookCow_pos_2, camera_lookCow_for_2),
                         animation.BasicPos(camera_lookCow_pos_2, camera_lookCow_for_2), 30)
bal.addAnimation("camera", ba)
# cow move
# camera follow
ba = animation.BasicAnim(animation.BasicPos(camera_lookCow_pos_2, camera_lookCow_for_2),
                         animation.BasicPos(camera_lookCow_pos_2, camera_lookCow_for_2), 120)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookCow_pos_2, camera_lookCow_for_2),
                         animation.BasicPos(camera_lookCowLeft_pos_1, camera_lookCowLeft_for_1), 30)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookCowLeft_pos_1, camera_lookCowLeft_for_1),
                         animation.BasicPos(camera_lookCowLeft_pos_2, camera_lookCowLeft_for_2), 30)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookCowLeft_pos_2, camera_lookCowLeft_for_2),
                         animation.BasicPos(camera_lookCowLeft_pos_2, camera_lookCowLeft_for_2), 60)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookCowLeft_pos_2, camera_lookCowLeft_for_2),
                         animation.BasicPos(camera_lookCowLeft_pos_1, camera_lookCowLeft_for_1), 90)
bal.addAnimation("camera", ba)
ba = animation.BasicAnim(animation.BasicPos(camera_lookCowLeft_pos_1, camera_lookCowLeft_for_1),
                         animation.BasicPos(camera_oriPos, camera_oriFor), 120)
bal.addAnimation("camera", ba)
# cow animation
ba = animation.BasicAnim(animation.BasicPos(cow_oriPos, Point()),
                         animation.BasicPos(cow_oriPos, Point()), 630)
bal.addAnimation("cow.obj", ba)
ba = animation.BasicAnim(animation.BasicPos(cow_oriPos, Point()),
                         animation.BasicPos(cow_newPos, Point()), 60)
bal.addAnimation("cow.obj", ba)

bal.beginAnmiation()


fileResolver = Thread.getThread().getFileResolver()
paramMap = StringMap()

scheduler = Scheduler.getInstance()
for i in range(0, multiprocessing.cpu_count()):
    scheduler.registerWorker(LocalWorker(i, 'wrk%i' % i))
scheduler.start()
totalFrames = 1111
# upper_filepath = os.path.abspath(os.path.join(os.getcwd(), "../.."))
for i in range(totalFrames):
    origin_now, target_now = bal.update("camera")
    processXML.changeXML_lookat(
        "scene_integrator_cam.xml", "perspective", origin_now, target_now)
    processXML.changeXML_translate(
        "scene_objs.xml", "cow.obj",  bal.update("cow.obj")[0])
    paramMap = StringMap()
    scene = SceneHandler.loadScene(
        fileResolver.resolve("scene_main.xml"), paramMap)
    queue = RenderQueue()
    scene.setDestinationFile('imgs/' + str(i) + '.jpg')
    # Create a render job and insert it into the queue
    job = RenderJob('myRenderJob', scene, queue)

    # render one img
    job.start()
    # Wait for all jobs to finish and release resources
    queue.waitLeft(0)
    queue.join()
