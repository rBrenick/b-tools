__author__ = "rBrenick"
__created__ = "2017-12-04"
__modifed__ = "2017-12-04"


import pymel.core as pm
import random as rand


"""
ex:

from bTools.animation import noise_generator
noise_generator.run()


"""


def get_time_range():
    start_time = int(pm.playbackOptions(q=True, min=True))
    end_time = int(pm.playbackOptions(q=True, max=True))
    return start_time, end_time


def generate_random_vector(weights=(1, 1, 1)):
    """
    Creates a Vec3 with the weight values as min and max
    :param weights: 
    :return: 
    """
    vector = []
    for w in weights:
        vector.append(rand.uniform(-w, w))
    return vector


def make_shake(objects=None, translate_weight=(1, 1, 1), rotate_weight=(1, 1, 1), key_distance=1, relative=True):
    """
    Saves all the transform data for each frame and adds a random vector offset to the translation and rotation values
    :param objects: 
    :param translate_weight: multiplier for the size of the generated vector
    :param rotate_weight:
    :param key_distance: amount of frames between each key
    :param relative: whether to add the values for each frame or just overwrite them
    :return: 
    """
    if not objects:
        objects = pm.selected(type="transform")

    start_time, end_time = get_time_range()

    pre_shake_transforms = {}

    pm.currentTime(start_time)
    for i in range(start_time, end_time):
        current_time = pm.currentTime(q=True)

        if current_time > end_time:
            break

        object_transforms = {}
        for obj in objects:
            org_transform = dict()
            org_transform["translate"] = list(obj.getTranslation())
            org_transform["rotate"] = list(obj.getRotation())
            org_transform["scale"] = obj.getScale()
            org_transform["node"] = obj

            object_transforms[obj.name()] = org_transform

        pre_shake_transforms[current_time] = object_transforms

        # Next frame
        pm.currentTime(current_time + key_distance)

    for frame in pre_shake_transforms.keys():

        pm.currentTime(frame)

        for obj, transform in pre_shake_transforms.get(frame).items():
            translate_rand_vec = generate_random_vector(translate_weight)
            rotation_rand_vec = generate_random_vector(rotate_weight)

            if relative:
                result_translation = [a+b for a, b in zip(translate_rand_vec, transform.get("translate"))]
                result_rotation = [a+b for a, b in zip(rotation_rand_vec, transform.get("rotate"))]
            else:
                result_translation = translate_rand_vec
                result_rotation = rotation_rand_vec

            transform.get("node").setTranslation(result_translation)
            transform.get("node").setRotation(result_rotation)

        pm.setKeyframe(objects, attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"])


class NoiseGenerator_UI(object):
    def __init__(self):
        win_title = "NoiseGenerator_V2"

        if pm.window(win_title, exists=True):
            pm.deleteUI(win_title)

        self.data = NoiseGenerator()

        self.strengthSlider = None
        self.keyDistanceSlider = None
        self.relativeCheckbox = None
        self.targetsList = None
        self.translationMultiplierSlider = None
        self.rotationMultiplierSlider = None

        self.translateSliders = []
        self.rotateSliders = []

        self.win = pm.window(win_title)
        self.setup_ui()

        # self.setTargets()
        self.win.show()

    def setup_ui(self):
        slider_params = dict()
        slider_params["field"] = True
        slider_params["min"] = 0
        slider_params["max"] = 1
        slider_params["fmn"] = -500
        slider_params["fmx"] = 500
        slider_params["value"] = 0.5
        slider_params["sliderStep"] = 0.01

        main_layout = pm.verticalLayout()

        with pm.verticalLayout():
            self.strengthSlider = pm.floatSliderGrp(label="Strength: ", **slider_params)
            self.keyDistanceSlider = pm.intSliderGrp(label="Key Distance: ", field=True, min=1, max=30, fmx=5000, v=3)
            self.relativeCheckbox = pm.checkBox(label='Relative (Additive)', value=True)
            pm.separator(style='in')

        with pm.verticalLayout():
            slider_params["enable"] = False

            # Translation Sliders
            slider_params["value"] = 1
            pm.checkBox(label='Set Translation Multipliers', changeCommand=self.toggle_translate_sliders)
            self.translationMultiplierSlider = pm.floatSliderGrp(label="Translation Multiplier: ", **slider_params)
            for axis in ["X", "Y", "Z"]:
                t_slider = pm.floatSliderGrp(label="Translate {}: ".format(axis), **slider_params)
                self.translateSliders.append(t_slider)

            pm.separator(style='in')

            # Rotation Sliders
            pm.checkBox(label='Set Rotation Multipliers', changeCommand=self.toggle_rotate_sliders)
            self.rotationMultiplierSlider = pm.floatSliderGrp(label="Rotation Multiplier", **slider_params)
            slider_params["max"] = 45
            slider_params["value"] = 45
            for axis in ["X", "Y", "Z"]:
                rSlider = pm.floatSliderGrp(label="Rotate {}: ".format(axis), **slider_params)
                self.rotateSliders.append(rSlider)

        pm.separator(style='in', height=20)

        # with pm.verticalLayout():
        #     targetsLayout = pm.horizontalLayout()
        #     with targetsLayout:
        #         self.targetsList = pm.textScrollList()
        #         pm.button("Set Targets", c=self.setTargets)

        # with pm.verticalLayout():
        pm.button("Make Some Noise", c=self.make_shake, backgroundColor=[0.2, 0.25, 0.49])
        # pm.button("Reset Settings")

        main_layout.redistribute(1, 1, 1)

    def set_targets(self, *args):
        """
        Sets the targets and fills the list in the UI
        :param args: 
        :return: 
        """
        targets = self.data.set_targets()
        # if self.targetsList:
        #     self.targetsList.removeAll()
        #     for target in targets:
        #         self.targetsList.append(target.nodeName())
        return targets

    def toggle_translate_sliders(self, *args):
        """
        Sets the enable state of the translation multiplier sliders
        :return: 
        """
        state = args[0]
        self.translationMultiplierSlider.setEnable(state)
        for slider in self.translateSliders:
            slider.setEnable(state)

    def toggle_rotate_sliders(self, *args):
        """
        Sets the enable state of the rotation multiplier sliders
        :return: 
        """
        state = args[0]
        self.rotationMultiplierSlider.setEnable(state)
        for slider in self.rotateSliders:
            slider.setEnable(state)

    def make_shake(self, *args):
        """
        GRabs the settings from the UI and launches the makeShake function from the data class
        :param args: 
        :return: 
        """
        # if not self.targetsList.getAllItems():
        self.set_targets()

        # Grab all the settings from the UI
        translation_strength = self.strengthSlider.getValue() * self.translationMultiplierSlider.getValue()
        rotation_strength = self.strengthSlider.getValue() * self.rotationMultiplierSlider.getValue()

        translate_weight = []
        for slider in self.translateSliders:
            translate_weight.append(slider.getValue()*translation_strength)

        rotate_weight = []
        for slider in self.rotateSliders:
            rotate_weight.append(slider.getValue()*rotation_strength)

        self.data.translationWeight = translate_weight
        self.data.rotationWeight = rotate_weight
        self.data.keyDistance = self.keyDistanceSlider.getValue()
        self.data.relative = self.relativeCheckbox.getValue()

        # Trigger Function
        self.data.make_shake()


class NoiseGenerator(object):
    def __init__(self):
        self.keyDistance = 1
        self.relative = True
        self.targets = []
        self.translationWeight = (1, 1, 1)
        self.rotationWeight = (1, 1, 1)

    def set_targets(self):
        self.targets = pm.selected(type="transform")
        return self.targets

    def validate_targets(self):
        for target in self.targets:
            if not pm.objExists(target):
                self.targets.pop(self.targets.index(target))

    def make_shake(self):
        self.validate_targets()
        if not self.targets:
            return

        make_shake(self.targets,
                   translate_weight=self.translationWeight,
                   rotate_weight=self.rotationWeight,
                   key_distance=self.keyDistance,
                   relative=self.relative)


def run():
    return NoiseGenerator_UI()


if __name__ == '__main__':
    run()
