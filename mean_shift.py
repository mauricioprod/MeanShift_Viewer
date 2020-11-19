from pathlib import Path
import cv2
import sys
import os
from PyQt5 import QtGui, QtCore, QtWidgets
import pymeanshift as pms
from ui.layout import Ui_MainWindow as MainWindow


# qt5 imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QTableWidgetItem
from PyQt5.QtGui     import QPixmap
from PyQt5.QtCore    import Qt

class MeanShiftGUI(QMainWindow, MainWindow):

    def __init__(self, parent=None):
        super(MeanShiftGUI, self).__init__(parent)

        self.setupUi(self)
        self.setup()

    def setup(self):

        # Setting the dialog
        self.file_dialog = QFileDialog()

        # Setting the graphic widget
        self.graphicsscene = QGraphicsScene()
        self.graphicsView.setScene(self.graphicsscene)
        self.graphicsscene_out = QGraphicsScene()
        self.outView.setScene(self.graphicsscene_out)

        self.is_loaded = False
        self.is_processed = False
        self.path = '~'
        self.range   = 10
        self.spatial = 10
        self.density = 100

    @QtCore.pyqtSlot()
    def open_file(self):

        # Get image path
        self.filename = self.file_dialog.getOpenFileName(self, "Select your image", 
                                                         os.path.expanduser(self.path),
                                                         "Images (*.png *.xpm *.jpg)")[0]
        self.path     = str(Path(self.filename).parents[0])

        # set filename to text edit
        self.load_textEdit.setText(self.filename)

        # Read image
        self.image = cv2.imread(self.filename)

        # Convert image
        self.image_in  = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()

        # Fix aspect ratio    
        pixmap_in  = QPixmap(self.image_in)
        viewWidth  = self.graphicsView.frameGeometry().width()
        viewHeight = self.graphicsView.frameGeometry().height()

        # Scaling in
        pixRatioMap = pixmap_in.scaled(viewWidth, viewHeight, Qt.KeepAspectRatio)
        pixItem_in = QGraphicsPixmapItem(pixRatioMap)

        # Original
        self.graphicsscene.clear()
        self.graphicsscene.addItem(pixItem_in)
        self.graphicsscene.update()

        
        self.output_textBrowser.setText('Image successfully loaded.')
        self.is_loaded = True
        self.update_status()

    @QtCore.pyqtSlot()
    def update_status(self):
        
        self.range   = self.range_spinBox.value()
        self.spatial = self.spatial_spinBox.value()
        self.density = self.density_spinBox.value()

        if self.is_loaded:
            self.apply_pushButton.setEnabled(True)
            self.range_spinBox.setEnabled(True)
            self.spatial_spinBox.setEnabled(True)
            self.density_spinBox.setEnabled(True)

        if self.is_processed:
            self.save_pushButton.setEnabled(True)
            self.apply_pushButton.setEnabled(True)


    @QtCore.pyqtSlot()
    def update_image(self):

        # Warning
        self.output_textBrowser.clear()
        self.output_textBrowser.setText('Image being precessed. Please wait.')
        self.apply_pushButton.setEnabled(False)

        # Processing
        (segmented_image, labels_image, number_regions) =  pms.segment(self.image, spatial_radius=self.spatial, 
                                                                      range_radius=self.range, min_density=self.density)
        self.image_seg = segmented_image


        # Convert image
        self.image_out  = QtGui.QImage(self.image_seg.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()

        # Update image
        pixmap_out = QPixmap(self.image_out)

        # Fix aspect ratio    
        viewWidth  = self.graphicsView.frameGeometry().width()
        viewHeight = self.graphicsView.frameGeometry().height()

        # Scaling out
        pixRatioMap_out = pixmap_out.scaled(viewWidth, viewHeight, Qt.KeepAspectRatio)
        pixItem_out = QGraphicsPixmapItem(pixRatioMap_out)

        # Output
        self.graphicsscene_out.clear()
        self.graphicsscene_out.addItem(pixItem_out)
        self.graphicsscene_out.update()

        # Set text output
        self.output_textBrowser.setText('Number of regions: {} .'.format(number_regions))
        self.is_processed = True
        self.update_status()
    
    @QtCore.pyqtSlot()
    def save_image(self):

        out_filename = '.'.join(self.filename.split('.')[:-1])  + '_r{0:03d}_s{0:03d}_d{0:03d}_out.png'.format(self.range, self.spatial, self.density)
        cv2.imwrite(out_filename, self.image_seg)

        self.output_textBrowser.setText('Segmented image successfully saved.')


if __name__ == '__main__':

    # Initializes the window system and constructs an application 
    app = QApplication(sys.argv)

    # Creating a GUI object
    win = MeanShiftGUI()
    win.show()

    # Refresh the GUI
    sys.exit(app.exec_())