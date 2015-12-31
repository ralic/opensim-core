import os
import unittest

import opensim as osim

test_dir = os.path.join(os.path.dirname(os.path.abspath(osim.__file__)),
                        'tests')

# TODO append
# TODO __setitem__

class TestStatesTrajectory(unittest.TestCase):
    states_sto_fname = "test_states_trajectory_gait1018_states.sto"
    def test_index_and_iterator(self):

        if os.path.exists(self.states_sto_fname):
            os.remove(self.states_sto_fname)

        model = osim.Model(os.path.join(test_dir,
            "gait10dof18musc_subject01.osim"))
        model.initSystem()

        forward = osim.ForwardTool()
        forward.setModel(model)
        forward.setName('test_states_trajectory_gait1018')
        forward.setFinalTime(0.1)
        forward.run()

        states = osim.StatesTrajectory.createFromStatesStorage(
                model, self.states_sto_fname)

        # Test indexing into the states container.
        model.getTotalMass(states[0])

        for i in range(states.getSize()):
            model.calcMassCenterVelocity(states.get(i))

        # Test iterator.
        for state in states:
            model.calcMassCenterPosition(state)

    def test_modify_states(self):
        model = osim.Model(os.path.join(test_dir,
            "gait10dof18musc_subject01.osim"))
        model.initSystem()

        states = osim.StatesTrajectory.createFromStatesStorage(
                model, self.states_sto_fname)

        states[0].setTime(4)
        assert states[0].getTime() == 4

        self.assertNotAlmostEqual(model.getStateVariableValue(states[2],
                "ground_pelvis/pelvis_tilt/value"), 8)
        model.setStateVariableValue(states[2],
                "ground_pelvis/pelvis_tilt/value", 8)
        self.assertAlmostEqual(model.getStateVariableValue(states[2],
                "ground_pelvis/pelvis_tilt/value"), 8)

        # Assigning is not allowed, since it easily allows people to violate
        # the ordering of the trajectory.
        # Also, the assignment `states.upd(5) = states[2]` is not possible in
        # Python ('can't assign to function call').
        def test_setitem():
            states[5] = states[2]
        self.assertRaises(TypeError, test_setitem)


    def test_states_storage_optional_arguments(self):
        # Try all combinations of optional arguments, just to ensure the
        # wrapping works.
        model = osim.Model(os.path.join(test_dir,
            "gait10dof18musc_subject01.osim"))
        sto = osim.Storage(self.states_sto_fname)
        states = osim.StatesTrajectory.createFromStatesStorage(
                model, sto)
        states = osim.StatesTrajectory.createFromStatesStorage(
                model, sto, False, False)
        states = osim.StatesTrajectory.createFromStatesStorage(
                model, sto, False, True)
        states = osim.StatesTrajectory.createFromStatesStorage(
                model, sto, True, False)
        states = osim.StatesTrajectory.createFromStatesStorage(
                model, sto, True, True)

    def test_populate_trajectory(self):
        model = osim.Model(os.path.join(test_dir,
            "gait10dof18musc_subject01.osim"))
        state = model.initSystem()
        states = osim.StatesTrajectory()
        states.append(state)
        state.setTime(1.0)
        states.append(state)

        self.assertEqual(states.getSize(), 2)
        self.assertEqual(states[1].getTime(), 1.0)

    def test_out_of_range(self):
        model = osim.Model(os.path.join(test_dir,
            "gait10dof18musc_subject01.osim"))
        state = model.initSystem()
        states = osim.StatesTrajectory()
        states.append(state)
        state.setTime(1.0)
        states.append(state)

        # TODO this exception message could be better...
        self.assertRaises(RuntimeError, lambda: states[2].getTime())











