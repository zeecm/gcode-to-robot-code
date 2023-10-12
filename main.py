from gcode_to_robot_code.abb.gcode_to_abb import ABBModuleGenerator
from gcode_to_robot_code.gcode_reader import GcodeReader

ELLIPSE_FILEPATH = "gcode_to_robot_code/gcode_files/EllipseV3.gcode"

if __name__ == "__main__":
    reader = GcodeReader()
    model = reader.read_file(ELLIPSE_FILEPATH)
    model.plot_path(projection="3d")
    gen = ABBModuleGenerator(model, module_name="Ellipse", procedure_name="DrawEllipse")
    gen.generate_robtargets_and_movements()
    gen.save_module()
