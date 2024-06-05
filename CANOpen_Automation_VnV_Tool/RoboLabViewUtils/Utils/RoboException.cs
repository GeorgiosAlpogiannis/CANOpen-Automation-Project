using CAN.PC;
using System;
using System.Text;

namespace Roboteq.LabView.Utils
{
    public class RoboException : Exception
    {
        public RoboExceptionCode ErrorCode { get; }

        public RoboException(RoboExceptionCode errorCode)
        {
            ErrorCode = errorCode;
        }

        public RoboException(RoboExceptionCode errorCode, string message) : base(message)
        {
            ErrorCode = errorCode;
        }

        public RoboException(RoboExceptionCode errorCode, string message, Exception innerException) : base(message, innerException)
        {
            ErrorCode = errorCode;
        }

        internal RoboException(RoboExceptionCode errorCode, TPCANStatus status) : this(errorCode, FormatMessage(status))
        {
        }

        public static string FormatMessage(TPCANStatus error)
        {
            var strTemp = new StringBuilder(256);

            if (PCANBasic.GetErrorText(error, 0, strTemp) != TPCANStatus.PCAN_ERROR_OK)
                return $"PCAN-{error:X}";
            else
                return strTemp.ToString();
        }
    }

    public enum RoboExceptionCode
    {
        NoError = 0,
        PCANError = 1,
        ErrorAlreadyConnected = 2,
        PCANErrorInitializing = 3,
        PCANErrorRegisterHandler = 4,
        ErrorGettingConfig = 5,
        ErrorCommandNotFound = 6,
        ErrorCommandNotNumeric = 7,
        ErrorCommandNotString = 8,
        ErrorCommandNotReadable = 9,
        ErrorCommandNotWritable = 10,
    }
}
