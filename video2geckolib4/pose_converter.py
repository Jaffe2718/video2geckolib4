from typing import NamedTuple, Iterable, List, Dict

import numpy as np
from scipy.spatial.transform import Rotation as R


BONES = ["Body", "Head", "LeftUpperArm", "LeftForearm", "LeftThigh", "LeftCalf", "RightUpperArm", "RightForearm", "RightThigh", "RightCalf"]


def _normalize(v: np.ndarray) -> np.ndarray:
    """
    Normalize a numpy array to [0, 1].
    """
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm


def _p(landmarks: NamedTuple, idx: int) -> np.ndarray:
    """
    Get point coordinate from landmarks
    :param landmarks: pose world landmarks
    :param idx: Index of pose landmarks
    :return: [x, y, z] coordinates in Blockbench coordinate system (row vector)
    """
    return -np.array([landmarks[idx].x, landmarks[idx].y, landmarks[idx].z], dtype=np.longdouble)


def _v(landmarks: NamedTuple, _from: int, _to: int) -> np.ndarray:
    """
    Calculate vector from _from to _to
    :param landmarks: pose world landmarks
    :param _from: Index of pose landmarks
    :param _to: Index of pose landmarks
    :return: [x, y, z] coordinates in Blockbench coordinate system (row vector)
    """
    return _p(landmarks, _to) - _p(landmarks, _from)


def _dist(landmarks: NamedTuple, _from: int, _to: int) -> float:
    return np.linalg.norm(_p(landmarks, _from) - _p(landmarks, _to))


def _euler_angles(rot_mat: np.ndarray) -> List[float]:
    """
    In Blockbench, if you face to the NORTH, your right is positive X, and your up is positive Y, and you are
    looking at the negative Z. Therefore, we define your right as relative X axis, and your up as relative Y axis,
    the relative Z axis is the direction opposite to your view direction.

    We use a rotation matrix to calculate the euler angles. X -> pitch, Y -> yaw, Z -> roll. In Blockbench, the rotation
    order is Z(roll) -> Y(yaw) -> X(pitch).

    :param rot_mat: rotation matrix (3x3), each row is identity vector [rx, ry, rz]
    :return: [Pitch, Yaw, Roll] (degrees)
    """
    r = R.from_matrix(rot_mat)
    roll, yaw, pitch = r.as_euler('ZYX', degrees=True)
    return [pitch, yaw, roll]

def _rel(cood_sys: np.ndarray, points: np.ndarray) -> np.ndarray:
    """
    calculate relative coordinate
    :param cood_sys:  system matrix (3x3), each row is identity vector [rx, ry, rz]
    :param points: nx3 matrix, each row is a point [x, y, z]
    :return: nx3 matrix, each row is a point [x, y, z] in relative coordinate
    """
    return cood_sys.T @ points


def _smooth_angle(base: float, angle: float) -> float:
    """
    Smooth angle to avoid sudden change
    :param base: base angle (degrees)
    :param angle: angle to smooth (degrees)
    :return: smooth angle (degrees)
    """
    delta = angle - base
    while delta > 180:
        angle -= 360
        delta = angle - base
    while delta < -180:
        angle += 360
        delta = angle - base
    return angle


class PoseConverter:
    """
    Convert pose landmarks to Blockbench rotation angles and translation vectors
    """

    @staticmethod
    def convert_pose(lm: NamedTuple) -> Dict[str, List[float]]:
        """
        convert pose landmarks to Blockbench rotation angles
        :param lm: pose landmarks
        :return: rotation angles dictionary (keys are BONES)
        """
        ans = {}

        # Body
        body_y = _v(lm, 24, 12) + _v(lm, 23, 11)
        body_z = np.cross(_v(lm, 23, 12), _v(lm, 24, 11))
        body_x = np.cross(body_y, body_z)
        body_sys = np.vstack([_normalize(body_x), _normalize(body_y), _normalize(body_z)]).T
        ans["Body"] = _euler_angles(body_sys)

        # Head (rel to Body)
        head_x = _v(lm, 9, 10) + _v(lm, 3, 6)
        head_z = np.cross(_v(lm, 9, 6), _v(lm, 10, 3))
        head_y = np.cross(head_z, head_x)
        head_sys = np.vstack([_normalize(head_x), _normalize(head_y), _normalize(head_z)]).T
        ans["Head"] = _euler_angles(_rel(body_sys, head_sys))
        ans["Head"][0] = -ans["Head"][0]

        # LeftUpperArm (rel to Body)
        left_upper_arm_y = _v(lm, 13, 11)
        left_upper_arm_x = np.cross( left_upper_arm_y, _v(lm, 15, 13))
        left_upper_arm_z = np.cross(left_upper_arm_x, left_upper_arm_y)
        left_upper_arm_sys = np.vstack([_normalize(left_upper_arm_x), _normalize(left_upper_arm_y), _normalize(left_upper_arm_z)]).T
        ans["LeftUpperArm"] = _euler_angles(_rel(body_sys, left_upper_arm_sys))

        # LeftForearm (rel to LeftUpperArm)
        left_forearm_y = _v(lm, 19, 13)
        left_forearm_x = np.cross(left_forearm_y, _v(lm, 21, 17))
        left_forearm_z = np.cross(left_forearm_x, left_forearm_y)
        left_forearm_sys = np.vstack([_normalize(left_forearm_x), _normalize(left_forearm_y), _normalize(left_forearm_z)]).T
        ans["LeftForearm"] = _euler_angles(_rel(left_upper_arm_sys, left_forearm_sys))

        # LeftThigh (rel to Body)
        left_thigh_y = _v(lm, 25, 23)
        left_thigh_z = np.cross(left_forearm_y, _v(lm, 24, 23))
        left_thigh_x = np.cross(left_thigh_y, left_thigh_z)
        left_thigh_sys = np.vstack([_normalize(left_thigh_x), _normalize(left_thigh_y), _normalize(left_thigh_z)]).T
        ans["LeftThigh"] = _euler_angles(_rel(body_sys, left_thigh_sys))

        # LeftCalf (rel to LeftThigh)
        left_calf_y = _v(lm, 27, 25)
        left_calf_z = np.cross(left_calf_y, _v(lm, 24, 23))
        left_calf_x = np.cross(left_calf_y, left_calf_z)
        left_calf_sys = np.vstack([_normalize(left_calf_x), _normalize(left_calf_y), _normalize(left_calf_z)]).T
        ans["LeftCalf"] = _euler_angles(_rel(left_thigh_sys, left_calf_sys))

        # RightUpperArm (rel to Body)
        right_upper_arm_y = _v(lm, 14, 12)
        right_upper_arm_x = np.cross(right_upper_arm_y, _v(lm, 16, 14))
        right_upper_arm_z = np.cross(right_upper_arm_x, right_upper_arm_y)
        right_upper_arm_sys = np.vstack([_normalize(right_upper_arm_x), _normalize(right_upper_arm_y), _normalize(right_upper_arm_z)]).T
        ans["RightUpperArm"] = _euler_angles(_rel(body_sys, right_upper_arm_sys))

        # RightForearm (rel to RightUpperArm)
        right_forearm_y = _v(lm, 20, 14)
        right_forearm_x = np.cross(right_forearm_y, _v(lm, 22, 18))
        right_forearm_z = np.cross(right_forearm_x, right_forearm_y)
        right_forearm_sys = np.vstack([_normalize(right_forearm_x), _normalize(right_forearm_y), _normalize(right_forearm_z)]).T
        ans["RightForearm"] = _euler_angles(_rel(right_upper_arm_sys, right_forearm_sys))

        # RightThigh (rel to Body)
        right_thigh_y = _v(lm, 26, 24)
        right_thigh_z = np.cross(right_thigh_y, _v(lm, 24, 23))
        right_thigh_x = np.cross(right_thigh_y, right_thigh_z)
        right_thigh_sys = np.vstack([_normalize(right_thigh_x), _normalize(right_thigh_y), _normalize(right_thigh_z)]).T
        ans["RightThigh"] = _euler_angles(_rel(body_sys, right_thigh_sys))

        # RightCalf (rel to RightThigh)
        right_calf_y = _v(lm, 28, 26)
        right_calf_z = np.cross(right_calf_y, _v(lm, 24, 23))
        right_calf_x = np.cross(right_calf_y, right_calf_z)
        right_calf_sys = np.vstack([_normalize(right_calf_x), _normalize(right_calf_y), _normalize(right_calf_z)]).T
        ans["RightCalf"] = _euler_angles(_rel(right_thigh_sys, right_calf_sys))

        return ans

    @staticmethod
    def apply_translation(landmark_frames: Iterable[NamedTuple]) -> List[List[float]]:
        """
        Apply translation to all frames, the landmarks in `landmark_frames` should be `pose_landmarks`
         but not `pose_world_landmarks`
        :param landmark_frames: an iterable of namedtuple objects, each object contains the pose landmarks of a frame
        :return: [[x, y, z], ...] where x, y, z is the translation vector in Blockbench coordinate system
        """
        translation_frames = []
        stat = PoseConverter.statistic_skeleton(landmark_frames)
        scale = 12 / stat["Body"]    # in Blockbench, body height is 12px
        p_center = np.array([stat["AverageX"], stat["AverageY"], stat["AverageZ"]])
        for lm in landmark_frames:
            trans = ((_p(lm, 23) + _p(lm, 24)) / 2 - p_center) * scale * np.array([-1, 1, 1])
            translation_frames.append(trans.astype(float).tolist())
        return translation_frames


    @staticmethod
    def calculate_poses(landmark_frames: Iterable[NamedTuple], smooth: bool = True) -> List[Dict[str, List[float]]]:
        """
        Calculate rotation angles for all frames
        :param landmark_frames: an iterable of namedtuple objects, each object contains the pose landmarks of a frame
        :param smooth: whether to smooth the rotation angles
        :return: a list of rotation angles dictionary (keys are BONES)
        """
        pose_frames = list(map(PoseConverter.convert_pose, landmark_frames))
        if smooth:
            for i in range(len(pose_frames) - 1):  # smooth the rotation angles
                pose, next_pose = pose_frames[i], pose_frames[i + 1]
                for bone in BONES:
                    for axis in range(3):
                        next_pose[bone][axis] = _smooth_angle(pose[bone][axis], next_pose[bone][axis])
        return pose_frames

    @staticmethod
    def statistic_skeleton(landmark_frames: Iterable[NamedTuple]) -> Dict[str, float]:
        """
        Statistic the average length and position of skeleton
        :param landmark_frame: an iterable of namedtuple objects, each object contains the pose landmarks of a frame
        :return: a dictionary with the average length of the skeleton
        """
        data = {}
        stat = {}
        for key in BONES:
            data[key] = []
        data["AverageX"] = []
        data["AverageY"] = []
        data["AverageZ"] = []
        for lm in landmark_frames:
            data["Body"].append((_dist(lm, 11, 23) + _dist(lm, 12, 24)) / 2)
            data["Head"].append(_dist(lm, 7, 8))
            data["LeftUpperArm"].append(_dist(lm, 11, 13))
            data["LeftForearm"].append(_dist(lm, 13, 19))
            data["LeftThigh"].append(_dist(lm, 25, 23))
            data["LeftCalf"].append(_dist(lm, 29, 25))
            data["RightUpperArm"].append(_dist(lm, 12, 14))
            data["RightForearm"].append(_dist(lm, 14, 20))
            data["RightThigh"].append(_dist(lm, 26, 24))
            data["RightCalf"].append(_dist(lm, 30, 26))

            x, y, z = (_p(lm, 23) + _p(lm, 24)) / 2
            data["AverageX"].append(x)
            data["AverageY"].append(y)
            data["AverageZ"].append(z)
        for key in data.keys():
            stat[key] = np.mean(data[key])
        return stat