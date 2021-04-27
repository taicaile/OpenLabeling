
def with_qt_test():
    try:
        import cv2
        WINDOW_NAME = "__WITH_QT_TEST__"
        cv2.namedWindow(WINDOW_NAME)
        cv2.displayOverlay(WINDOW_NAME, 'Test QT', 500)
        cv2.destroyWindow(WINDOW_NAME)
        return True
    except cv2.error:
        return False