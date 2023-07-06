import os
import h5py as h5
import numpy as np

route_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def quat2euler(quat):
    # TODO: import from SHARPy
    delta = quat[0]*quat[2] - quat[1]*quat[3]

    yaw = np.arctan(2*(quat[0]*quat[3]+quat[1]*quat[2])/(1-2*(quat[2]**2+quat[3]**2)))
    pitch = np.arcsin(2*delta)
    roll = np.arctan(2*(quat[0]*quat[1]+quat[2]*quat[3])/(1-2*(quat[1]**2+quat[2]**2)))

    return np.array([roll, pitch, yaw])


def get_time_history(output_folder, case):
    file = os.path.join(output_folder,
                         case, 
                        'savedata', 
                        case + '.data.h5')   
    with h5.File(file, "r") as f:
            ts_max = len(f['data']['structure']['timestep_info'].keys())-2
            dt = float(str(np.array(f['data']['settings']['DynamicCoupled']['dt'])))
            matrix_data = np.zeros((ts_max, 17))
            matrix_data[:,0] = np.array(list(range(ts_max))) * dt
            node_tip = np.argmax(np.array(f['data']['structure']['timestep_info']['00000']['pos'])[:,1])

            node_root = 0
            element_tip = int(np.round((node_tip - 1)/2. -0.1))

            for its in range(0,ts_max):
                ts_str = f'{its:05d}'
                matrix_data[its, 1] = np.array(f['data']['aero']['timestep_info'][ts_str]['u_ext']['00000'])[2,0,0] # Vertical gust velocity at LE
                matrix_data[its, 2:5] = np.array(f['data']['structure']['timestep_info'][ts_str]['pos'])[node_tip, :] # Displacements of tip node
                matrix_data[its, 5:8] = np.array(f['data']['structure']['timestep_info'][ts_str]['pos_dot'])[node_tip, :] # Velocity of tip node
                matrix_data[its, 8:11] = np.array(f['data']['structure']['timestep_info'][ts_str]['psi'])[element_tip, -1, :] # Rotations of tip node
                matrix_data[its, 11:14] = np.array(f['data']['structure']['timestep_info'][ts_str]['psi_dot'])[element_tip, -1, :] # Gradient of tip node rotation
                matrix_data[its, 14] = np.array(f['data']['structure']['timestep_info'][ts_str]['postproc_cell']['loads'])[node_root,4] # OOP root bending loads
                matrix_data[its, 15] = np.array(f['data']['structure']['timestep_info'][ts_str]['postproc_cell']['loads'])[node_root,3] # Torsional root bending loads
                matrix_data[its, 16] = np.deg2rad(quat2euler(np.array(f['data']['structure']['timestep_info'][ts_str]['quat'])))[1] # Aircraft Pitching Angle

    return matrix_data

def get_header(parameter_labels):
    header_parameter = 'time'
    for ilabel in range(len(parameter_labels)):
         header_parameter += ', {}'.format(parameter_labels[ilabel])
    return header_parameter 
     
def write_results(data, case,parameter_labels, result_folder):  
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    np.savetxt(os.path.join(os.path.join(result_folder, case + '.txt')), 
               data,
               fmt='%10e,' * (np.shape(data)[1] - 1) + '%10e', 
               delimiter=", ", 
               header= get_header(parameter_labels))


def main():         
    list_cases = [
        'superflexop_free_L_10_I_10',
                 ]
    SHARPY_output_folder = route_dir + '/lib/sharpy/output/'
    result_folder = route_dir + '/results_gust_response/'
    parameter_labels=  ['omega_z', 'x','y','z', 'x_dot','y_dot','z_dot', 
                        'r','p','q', 'r_dot','p_dot','q_dot',
                        'OOP', 'MT', 'Pitch']
    for case in list_cases:
        data = get_time_history(SHARPY_output_folder,  case)
        write_results(data, case, parameter_labels, result_folder)


if __name__ == '__main__':
    main()
