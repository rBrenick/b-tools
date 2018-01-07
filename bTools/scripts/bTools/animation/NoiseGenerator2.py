__author__ = "rBrenick"
__created__ = "2017-12-04"
__modifed__ = "2017-12-04"


import pymel.core as pm
import random as rand


"""
ex:

from animation import NoiseGeneratorV2; reload(NoiseGeneratorV2)
NoiseGeneratorV2.NoiseGenerator_UI()


"""


def getTimeRange():
    startTime = int(pm.playbackOptions(q=True, min=True))
    endTime = int(pm.playbackOptions(q=True, max=True))
    return startTime, endTime


def generateRandomVector(weights=(1, 1, 1)):
    """
    Creates a Vec3 with the weight values as min and max
    :param weights: 
    :return: 
    """
    vector = []
    for w in weights:
        vector.append(rand.uniform(-w, w))
    return vector


def makeShake(objects=None, translateWeight=(1,1,1), rotateWeight=(1,1,1), keyDistance=1, relative=True):
    """
    Saves all the transform data for each frame and adds a random vector offset to the translation and rotation values
    :param objects: 
    :param translateWeight: multiplier for the size of the generated vector 
    :param rotateWeight: 
    :param keyDistance: amount of frames between each key
    :param relative: whether to add the values for each frame or just overwrite them
    :return: 
    """
    if not objects:
        objects = pm.selected(type="transform")

    startTime, endTime = getTimeRange()

    preShakeTransforms = {}

    pm.currentTime(startTime)
    for i in range(startTime, endTime):
        currentTime = pm.currentTime(q=True)

        if currentTime > endTime:
            break

        objectTransforms = {}
        for obj in objects:
            orgTransform = dict()
            orgTransform["translate"] = list(obj.getTranslation())
            orgTransform["rotate"] = list(obj.getRotation())
            orgTransform["scale"] = obj.getScale()
            orgTransform["node"] = obj

            objectTransforms[obj.name()] = orgTransform

        preShakeTransforms[currentTime] = objectTransforms

        # Next frame
        pm.currentTime(currentTime + keyDistance)

    for frame in preShakeTransforms.keys():

        pm.currentTime(frame)

        for obj, transform in preShakeTransforms.get(frame).items():
            transRandVec = generateRandomVector(translateWeight)
            rotRandVec = generateRandomVector(rotateWeight)

            if relative:
                resultTranslation = [a+b for a, b in zip(transRandVec, transform.get("translate"))]
                resultRotation = [a+b for a, b in zip(rotRandVec, transform.get("rotate"))]
            else:
                resultTranslation = transRandVec
                resultRotation = rotRandVec

            transform.get("node").setTranslation(resultTranslation)
            transform.get("node").setRotation(resultRotation)

        pm.setKeyframe(objects, attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"])


class NoiseGenerator_UI(object):
    def __init__(self):
        winTitle = "NoiseGenerator_V2"

        if pm.window(winTitle, exists=True):
            pm.deleteUI(winTitle)

        self.data = NoiseGenerator()

        self.strengthSlider = None
        self.keyDistanceSlider = None
        self.relativeCheckbox = None
        self.targetsList = None
        self.translationMultiplierSlider = None
        self.rotationMultiplierSlider = None

        self.translateSliders = []
        self.rotateSliders = []

        self.win = pm.window(winTitle)
        self.setupUI()

        # self.setTargets()
        self.win.show()

    def setupUI(self):
        sliderParams = dict()
        sliderParams["field"] = True
        sliderParams["min"] = 0
        sliderParams["max"] = 1
        sliderParams["fmn"] = -500
        sliderParams["fmx"] = 500
        sliderParams["value"] = 0.5
        sliderParams["sliderStep"] = 0.01

        mainLayout = pm.verticalLayout()

        with pm.verticalLayout():
            self.strengthSlider = pm.floatSliderGrp(label="Strength: ", **sliderParams)
            self.keyDistanceSlider = pm.intSliderGrp(label="Key Distance: ", field=True, min=1, max=30, fmx=5000, v=3)
            self.relativeCheckbox = pm.checkBox(label='Relative (Additive)', value=True)
            pm.separator(style='in')

        with pm.verticalLayout():
            sliderParams["enable"] = False

            # Translation Sliders
            sliderParams["value"] = 1
            pm.checkBox(label='Set Translation Multipliers', changeCommand=self.toggleTranslateSliders)
            self.translationMultiplierSlider = pm.floatSliderGrp(label="Translation Multiplier: ", **sliderParams)
            for axis in ["X", "Y", "Z"]:
                tSlider = pm.floatSliderGrp(label="Translate {}: ".format(axis), **sliderParams)
                self.translateSliders.append(tSlider)

            pm.separator(style='in')

            # Rotation Sliders
            pm.checkBox(label='Set Rotation Multipliers', changeCommand=self.toggleRotateSliders)
            self.rotationMultiplierSlider = pm.floatSliderGrp(label="Rotation Multiplier", **sliderParams)
            sliderParams["max"] = 45
            sliderParams["value"] = 45
            for axis in ["X", "Y", "Z"]:
                rSlider = pm.floatSliderGrp(label="Rotate {}: ".format(axis), **sliderParams)
                self.rotateSliders.append(rSlider)

        pm.separator(style='in', height=20)

        # with pm.verticalLayout():
        #     targetsLayout = pm.horizontalLayout()
        #     with targetsLayout:
        #         self.targetsList = pm.textScrollList()
        #         pm.button("Set Targets", c=self.setTargets)

        # with pm.verticalLayout():
        pm.button("Make Some Noise", c=self.makeShake, backgroundColor=[0.2, 0.25, 0.49])
            # pm.button("Reset Settings")

        mainLayout.redistribute(1, 1, 1)

    def setTargets(self, *args):
        """
        Sets the targets and fills the list in the UI
        :param args: 
        :return: 
        """
        targets = self.data.setTargets()
        # if self.targetsList:
        #     self.targetsList.removeAll()
        #     for target in targets:
        #         self.targetsList.append(target.nodeName())
        return targets

    def toggleTranslateSliders(self, *args):
        """
        Sets the enable state of the translation multiplier sliders
        :return: 
        """
        state = args[0]
        self.translationMultiplierSlider.setEnable(state)
        for slider in self.translateSliders:
            slider.setEnable(state)

    def toggleRotateSliders(self, *args):
        """
        Sets the enable state of the rotation multiplier sliders
        :return: 
        """
        state = args[0]
        self.rotationMultiplierSlider.setEnable(state)
        for slider in self.rotateSliders:
            slider.setEnable(state)

    def makeShake(self, *args):
        """
        GRabs the settings from the UI and launches the makeShake function from the data class
        :param args: 
        :return: 
        """
        # if not self.targetsList.getAllItems():
        self.setTargets()

        # Grab all the settings from the UI
        translationStrength = self.strengthSlider.getValue() * self.translationMultiplierSlider.getValue()
        rotationStrength = self.strengthSlider.getValue() * self.rotationMultiplierSlider.getValue()

        translateWeight = []
        for slider in self.translateSliders:
            translateWeight.append(slider.getValue()*translationStrength)

        rotateWeight = []
        for slider in self.rotateSliders:
            rotateWeight.append(slider.getValue()*rotationStrength)

        self.data.translationWeight = translateWeight
        self.data.rotationWeight = rotateWeight
        self.data.keyDistance = self.keyDistanceSlider.getValue()
        self.data.relative = self.relativeCheckbox.getValue()

        # Trigger Function
        self.data.makeShake()


class NoiseGenerator(object):
    def __init__(self):
        self.keyDistance = 1
        self.relative = True
        self.targets = []
        self.translationWeight = (1, 1, 1)
        self.rotationWeight = (1, 1, 1)

    def setTargets(self):
        self.targets = pm.selected(type="transform")
        return self.targets

    def validateTargets(self):
        for target in self.targets:
            if not pm.objExists(target):
                self.targets.pop(self.targets.index(target))

    def makeShake(self):
        self.validateTargets()
        if not self.targets:
            return

        makeShake(self.targets,
                  translateWeight=self.translationWeight,
                  rotateWeight=self.rotationWeight,
                  keyDistance=self.keyDistance,
                  relative=self.relative)

if __name__ == '__main__':
    NoiseGenerator_UI()
