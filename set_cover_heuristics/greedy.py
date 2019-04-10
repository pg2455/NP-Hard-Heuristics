import torch

def get_child_set_cover_problem(x, M, W):
    ones = torch.nonzero(x==1).flatten()
    zeros = torch.nonzero(x==0).flatten()
    undecided = torch.nonzero(x==-1).flatten()

    not_v = torch.arange(M.shape[0])
    if ones.shape[0]:
        not_v = torch.nonzero(torch.prod(M[:, ones] == 0, dim=1)).flatten()

    w = W[undecided]
    m = M[not_v,:][:,undecided]
    return m,w, W[ones].sum()

def approx_set_cover(M,W):
    m,w = M.clone(), W.clone()
    X = -torch.ones(w.shape)
    remain_vec = X == -1
    while m.numel() != 0:
        score = w / m.sum(dim=0)
        index = torch.argmin(score) # greedy

        x_tmp = X[remain_vec].clone()
        x_tmp[index]= 1
        X[remain_vec] = x_tmp

        m,w, c = get_child_set_cover_problem(X, M, W)
        remain_vec = X == -1
    X[remain_vec] = 0

    return X, W[X==1].sum()


if __name__ == "__main__":
    """
    M: |U| x N binary matrix
        U is the set containing all the elements
        N is the number of subsets - S1, S2, S3, .... SN
        For column i, all j s/t matrix(i,j) = 1 implies that Si contains element j
    """
    M = torch.Tensor([[1,0,1,0], [0,1,1,1],[1,0,0,1]])
    W = torch.Tensor([0.1, 0.2, 0.4, 0.5])
    print(approx_set_cover(M,W))
