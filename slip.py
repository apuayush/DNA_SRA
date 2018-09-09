def slip(coord, frame):
        import cv2
        import imutils

        slip = frame[coord[1]:coord[-1], coord[0]:coord[-2]]
        gray = cv2.cvtColor(slip, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        m = 0
        for c in cnts:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            m = max(abs(cX - 123), m)

        return m/123 * 100
