import cv2
import gym
import numpy as np
import torch
from proj1.model3 import Net
from time import sleep
from collections import deque
cv2.namedWindow('main', cv2.WINDOW_NORMAL)
cv2.namedWindow('diff', cv2.WINDOW_NORMAL)
cv2.namedWindow('pozadie', cv2.WINDOW_NORMAL)
cv2.namedWindow('diff2', cv2.WINDOW_NORMAL)
cv2.namedWindow('net', cv2.WINDOW_NORMAL)

# class Plan:
#     def __init__(self):
#
#     def show(self):

def main():
    if torch.cuda.is_available():
        dev = "cuda:0"
    else:
        dev = "cpu"
    dev = 'cpu'
    device = torch.device(dev)

    net = Net().to(device)
    criterion = torch.nn.MSELoss(reduction='sum')
    # optimizer = torch.optim.SGD(net.parameters(), lr=1e-4, momentum=0.9)
    # optimizer = torch.optim.SGD(net.parameters(), lr=0.0000001)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.0001)
    env = gym.make("procgen:procgen-heist-v0", start_level=0, num_levels=1)
    print(env.action_space)
    # net = None
    for i_episode in range(20):
        observation = env.reset()
        plan = [env.action_space.sample() for i in range(5)]
        prev_gs_image = None
        pozadie_rolling_average = None

        for t in range(10000):
            env.render()
            #print(observation)
            # bgr_image = cv2.cvtColor(observation, cv2.COLOR_RGB2BGR)
            # gs_image = cv2.cvtColor(observation, cv2.COLOR_RGB2GRAY) / 255
            # gs_image = (cv2.cvtColor(observation, cv2.COLOR_RGB2BGR)) / 255
            gs_image = cv2.cvtColor(observation, cv2.COLOR_RGB2BGR)
            gs_image = cv2.resize(gs_image, dsize=(32,32))
            print(gs_image[(0,0)])
            # if prev_gs_image is None:
            #     prev_gs_image = gs_image * 0
            # if net is None:
            #     net = Net(gs_image.shape)
            for u in range(10000):
                loss_sum = 0
                psnr_sum = 0
                for x in range(0, 32):
                    # loss_ = torch.Tensor([0]).to(device)
                    psnr_ = torch.Tensor([0]).to(device)

                    for y in range(0, 32):
                        coord = np.array([x, y])/32
                        pred_pix = net(torch.Tensor(coord).to(device))
                        loss = criterion(pred_pix, torch.Tensor(np.array(gs_image[(x, y)])/255).to(device))
                        # psnr = 10 * torch.log10(1 / loss)
                        # optimizer.zero_grad()
                        # print(f'Loss: {loss.detach()}')
                        # loss_ += loss
                        # psnr_ += psnr
                        loss_sum += loss.detach()
                        loss.backward()
                        optimizer.step()
                        optimizer.zero_grad()
                        # psnr_sum += psnr.detach()
                    # loss_.backward()
                    # psnr_.backward()
                    # optimizer.step()
                    cv2.waitKey(100)
                    # optimizer.zero_grad()
                print(u)
                # average loss where?
                # average loss where?
                print(f'Loss sum: {loss_sum}')
                # print(f'PSNR sum: {psnr_sum}')
                pred_image = np.zeros((32, 32, 3))
                print(pred_image.shape)
                for x in range(0, 32):
                    for y in range(0, 32):
                        coord = np.array([x, y])/32
                        pred_pix = net(torch.Tensor(coord).to(device)).detach()
                        pred_image[(x, y)] = pred_pix.to('cpu')
                cv2.imshow('net', pred_image * 255)
                gs = np.array(gs_image)
                cv2.imshow('main', gs)
                # cv2.imshow('net', np.array(pred_img.detach()))
                cv2.waitKey(100)
    env.close()


if __name__ == "__main__":
    main()