from numpy import *
import cv2

class Trifocal:
    def __init__(self, *args):
        '''Initialize with a set of 2 or 3 camera projection matrices (3x4 or 4x4)
        or with 3 sets of corresponding points (all 3xN).'''
        if args[0].shape == (3,4) or args[0].shape == (4,4):
            self.T, self.scale = self.tensor_P( list(args) )
        elif len(args) == 3 and args[0].shape[0] == 3:
            self.T, self.scale = self.tensor_pts( *args )
        else:
            raise Warning, 'Trifocal initialization failed!'

    def __call__(self, A, B, transpose=False):
        '''Method to pre and post multiply matrices to the tensor.'''
        if A == None: A = 1.
        if B == None: B = 1.
        return r_[[dot(dot(A,self.T[i]),B) for i in (0,1,2)]]

    def __str__(self):
        return str(self.T)

    # CONSTRAINT TESTING METHODS
    def lll(self, line1, line2, line3):
        return dot(self._ll(line2,line3), skew(line1))

    def pll(self, pt1, line2, line3):
        xT = sum([pt1[i]*self.T[i] for i in (0,1,2)],0)
        return dot(dot(line2,xT),line3)

    def plp(self, pt1, line2, pt3):
        xT = sum([pt1[i]*self.T[i] for i in (0,1,2)],0)
        return dot(dot(line2,xT),skew(pt3))

    def ppl(self, pt1, pt2, line3):
        xT = sum([pt1[i]*self.T[i] for i in (0,1,2)],0)
        return dot(dot(skew(pt2),xT),line3)

    def ppp(self, pt1, pt2, pt3):
        xT = sum([pt1[i]*self.T[i] for i in (0,1,2)],0)
        return dot(dot(skew(pt2),xT),skew(pt3))

    # LINE TRANSFER METHOD
    def _ll(self, line2, line3):
        '''Calculate point in 1st image from lines in 2nd and 3rd.'''
        return r_[[dot(dot(line2,self.T[i]),line3) for i in (0,1,2)]]

    # POINT TRANSFER METHODS
    def p_l(self, pt1, line3):
        '''Calculate point in 2nd image from point in 1st and line in 3rd.'''
        xT = sum([pt1[i]*self.T[i] for i in (0,1,2)],0)
        return dot(xT,line3)

    def pl_(self, pt1, line2):
        '''Calculate point in 3rd image from point in 1st and line in 2rd.'''
        xT = sum([pt1[i]*self.T[i] for i in (0,1,2)],0)
        return dot(line2,xT)

    def getEpipoles(self):
        '''Returns the epipole/position of camera 1 in image 2 and 3.'''
        u = r_[[cv2.SVDecomp(t.T)[2][-1] for t in self.T]]
        ei = cv2.SVDecomp(u)[2][-1]
        v = r_[[cv2.SVDecomp(t)[2][-1] for t in self.T]]
        eii = cv2.SVDecomp(v)[2][-1]
        return ei, eii

    def getFundamentalMat(self):
        '''Returns the f-mat of camera 2 to 1 and camera 3 to 1.'''
        ei,eii = self.getEpipoles()
        F21 = array([dot(dot(skew(ei),t),eii) for t in self.T]).T
        F31 = array([dot(dot(skew(eii),t.T),ei) for t in self.T]).T
        return F21, F31

    def getProjectionMat(self, from_E=True):
        ei,eii = self.getEpipoles()
        ei = cv2.normalize(ei).flatten()
        eii  = cv2.normalize(eii).flatten()
        if from_E == True:
            F21,F31 = self.getFundamentalMat()
            H21 = H_from_E(F21)
            H31 = H_from_E(F31)
            v1 = r_[0.5,0.5,50,1.]
            v2 = r_[1.,1.,51,1.]
            for H in H21:
                ln2 = cross(dot(H,v1)[:3],dot(H,v2)[:3])
                pt3 = self.pl_(v1[:3]/v1[3], ln2)
                pt3 /= pt3[2]
                print pt3
                for H2 in H31:
                    print dot(H2,v1)[:3]/dot(H2,v1)[:3][2]


            return H21,H31
        else:
            Pi = eye(4)
            Pi[:3,:3] = array([dot(t,eii) for t in self.T]).T
            Pi[:3,3] = ei
#            K = cv2.decomposeProjectionMatrix(Pi[:3])[0]
#            Pi[:3] = dot(cv2.invert(K)[1],Pi[:3])
            return Pi

    def tensor_pts(self, x0, x1, x2):
        '''Calculates tensor from point correspondences.'''
        N = len(x0[0])
        M = zeros((N*4,27))
        for i in range(N):
            for j in range(3):
                block = zeros((4,9))
                block[[0,1,0,1,2,3,2,3,0,2,1,3,0,1,2,3],
                      [0,1,2,2,3,4,5,5,6,6,7,7,8,8,8,8]] = x0[j,i]
                block[:2,6:] *= -x1[0,i]
                block[2:,6:] *= -x1[1,i]
                block[:2,2] *= -x2[:2,i]
                block[2:,5] *= -x2[:2,i]
                block[:2,8] *= -x2[:2,i]
                block[2:,8] *= -x2[:2,i]
                M[i*4:i*4+4, j*9:j*9+9] = block.copy()

        V = cv2.SVDecomp(M)[2]
        self.T = V[-1,:27].reshape((3,3,3))
        return self.T, 1.0

    def tensor_P(self, Plist):
        '''Calculates tensor from two camera projections.

        Plist is a list of 3x4 projections. If three are listed then the first is
        assumed to be the origin and not considered. If two are listed then it is
        assumed that the origin projection was omitted.'''
        try:
            if len(Plist) == 3:
                A = Plist[1][:3]
                B = Plist[2][:3]
            else:
                A = Plist[0][:3]
                B = Plist[1][:3]
        except:
            raise Warning, 'List of two or three 3x4 (or 4x4) projection matrices.'

        T = zeros((3,3,3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    T[i,j,k] = A[j,i]*B[k,3] - A[j,3]*B[k,i]
        scale = sqrt(sum(B[:3,3]**2))/sqrt(sum(A[:3,3]**2))
        return T, scale

def skew(v):
    if len(v) == 4: v = v[:3]/v[3]
    skv = roll(roll(diag(v.flatten()), 1, 1), -1, 0)
    return skv - skv.T

def H_from_E(E, RandT=False):
    '''Returns a 4x4x4 matrix of possible H translations.
    Or returns the two rotations and translation vectors when keyword is True.
    '''
    S,U,V = cv2.SVDecomp(E)
    #TIP: Recover E by dot(U,dot(diag(S.flatten()),V))
    W = array([[0,-1,0],[1,0,0],[0,0,1]])

    R1 = dot(dot(U,W),V)
    R2 = dot(dot(U,W.T),V)
    if cv2.determinant(R1) < 0:
        R1,R2 = -R1,-R2
    t1 = U[:,2]
    t2 = -t1

    if RandT:
        return R1, R2, t1, t2

    H = zeros((4,4,4))
    H[:2,:3,:3] = R1
    H[2:,:3,:3] = R2
    H[[0,2],:3,3] = t1
    H[[1,3],:3,3] = t2
    H[:,3,3] = 1

    return H
