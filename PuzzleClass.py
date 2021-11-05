import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sklearn
from show_pic import show_pic
from remove_element_from_array import remove_element_from_array
from rank_pieces_match import rank_pieces_match


class PuzzlePicture:

    def __init__(self, image_to_open, n_vertical_chunks, m_horizontal_chunks):
        self.n_vertical_chunks = n_vertical_chunks
        self.m_horizontal_chunks = m_horizontal_chunks
        self.image_to_open = image_to_open
        self.image = []
        self.color_image = []
        self.pieces = []
        self.color_pieces = []
        self._make_rectangular_puzzle()

    def _make_rectangular_puzzle(self):
        self._gray_color_pic()
        self._adjust_im_to_num_chunks()
        self._add_black_frame()
        self._chunk_im_to_pieces()
        self.shuffled_pieces_and_display()

    def display_piece_in_subplot(self, num_in_subplot, piece, fig, gray=0):
        fig.add_subplot(self.n_vertical_chunks, self.m_horizontal_chunks, num_in_subplot, xticks=[], yticks=[])
        fig.tight_layout()
        if gray:
            plt.imshow(np.uint8(piece), cmap='gray', vmin=0, vmax=255)
        else:
            plt.imshow(np.uint8(piece), vmin=0, vmax=255)
        plt.waitforbuttonpress()

    def _gray_color_pic(self):
        """convert the input puzzle picture to gray scale"""
        self.color_image = np.asarray(Image.open(self.image_to_open))
        self.image = np.asarray(Image.open(self.image_to_open).convert('L'))

    def _adjust_im_to_num_chunks(self):
        """remove rows and cols for later cutting to equaled pieces without remainder
         if needed, the rows and cols will remove from the up and left of the image, respectively"""
        shape_im = self.image.shape
        rows_remainder = shape_im[0] % self.n_vertical_chunks
        cols_remainder = shape_im[1] % self.m_horizontal_chunks
        if rows_remainder != 0:
            self.image = self.image[rows_remainder:, :]
            self.color_image = self.color_image[rows_remainder:, :, :]
        if cols_remainder != 0:
            self.image = self.image[:, cols_remainder:]
            self.color_image = self.color_image[:, cols_remainder:, :]

    def _add_black_frame(self):
        """add black frame to identify frame pieces later"""
        black_cols = np.zeros((len(self.image[:, 0]), self.m_horizontal_chunks))
        black_mat_cols = np.zeros((len(self.image[:, 0]), self.m_horizontal_chunks, 3))
        self.image = np.c_[black_cols, self.image, black_cols]
        self.color_image = np.concatenate([black_mat_cols, self.color_image, black_mat_cols], axis=1)
        black_rows = np.zeros((self.n_vertical_chunks, len(self.image[0, :])))
        black_mat_rows = np.zeros((self.n_vertical_chunks, len(self.image[0, :]), 3))
        self.image = np.vstack([black_rows, self.image, black_rows])
        self.color_image = np.concatenate([black_mat_rows, self.color_image, black_mat_rows], axis=0)

    def _chunk_im_to_pieces(self):
        """ get rectangular picture and split it to equaled pieces by input horizontal and vertical number of pieces"""
        shape_im = self.image.shape
        self.height_piece = shape_im[0] // self.n_vertical_chunks
        self.width_piece = shape_im[1] // self.m_horizontal_chunks
        num_in_subplot = 1
        pieces = []
        color_pieces = []
        for i in range(self.n_vertical_chunks):
            rows_mask_for_piece = np.arange(self.height_piece * i, self.height_piece * (i + 1))
            for j in range(self.m_horizontal_chunks):
                cols_mask_for_piece = np.arange(self.width_piece * j, self.width_piece * (j + 1))
                new_piece = self.image[rows_mask_for_piece][:, cols_mask_for_piece]
                new_color_piece = self.color_image[rows_mask_for_piece][:, cols_mask_for_piece, :]
                num_in_subplot += 1
                pieces.append(new_piece)
                color_pieces.append(new_color_piece)
        self.pieces = pieces
        self.color_pieces = color_pieces

    def shuffled_pieces_and_display(self):
        """randomized and display pieces"""
        self.pieces, self.color_pieces = sklearn.utils.shuffle(self.pieces, self.color_pieces)
        show_pic(self.color_pieces, self.m_horizontal_chunks)
        plt.waitforbuttonpress()

    def solve_puzzle(self):
        fig_solve = plt.figure(2, figsize=(6, 6))
        num_in_subplot = 1
        vertical_black_frame = np.zeros((1, self.width_piece))
        horizontal_black_frame = np.zeros((self.height_piece, 1))
        new_solved_piece = vertical_black_frame
        piece_above_spot = horizontal_black_frame
        solved_puzzle = []
        list_pieces = self.pieces
        for i_spot in range(self.n_vertical_chunks):
            for j_spot in range(self.m_horizontal_chunks):
                best_rank = np.inf
                if i_spot > 0:  # or ((i_spot == 0) and (j_spot == self.m_horizontal_chunks - 1)):
                    piece_above_spot = solved_puzzle[-self.m_horizontal_chunks]  # one line back to get piece above spot
                for piece in list_pieces:
                    self.display_piece_in_subplot(num_in_subplot, piece, fig_solve, 1)
                    rank_vrt = rank_pieces_match(new_solved_piece, piece, 'right')
                    rank_hrz = rank_pieces_match(piece_above_spot, piece, 'down')
                    tot_rank = rank_hrz + rank_vrt
                    if tot_rank < best_rank:  # minimum rank is the best
                        best_rank = tot_rank
                        cur_new_solved_piece = piece
                new_solved_piece = cur_new_solved_piece
                solved_puzzle.append(new_solved_piece)
                list_pieces, ind = remove_element_from_array(list_pieces, new_solved_piece)
                new_color_solved_piece = self.color_pieces[ind]
                self.color_pieces, ind = remove_element_from_array(self.color_pieces, new_color_solved_piece)
                self.display_piece_in_subplot(num_in_subplot, new_color_solved_piece, fig_solve)
                num_in_subplot += 1
        return solved_puzzle
