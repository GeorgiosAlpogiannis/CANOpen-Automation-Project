using CAN.PC;
using Roboteq.CommandsConfigurator.Helpers;
using Roboteq.CommandsConfigurator.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Roboteq.LabView.Utils
{
    public interface IProgress<in T>
    {
        void Report(T value);
    }
    public class RoboController
    {
        public readonly TimeSpan SdoTimeout = TimeSpan.FromSeconds(2);
        public event EventHandler<MessageEventArgs> MessageComposed = null;
        public event EventHandler<MessageEventArgs> MessageReceived = null;

        private byte currentNode;
        private ushort currentHandle;
        private RoboControllerBaudRate currentBaudRate;
        private CancellationTokenSource listenerCancellationSource;

        private TaskCompletionSource<CanMessage> bootupCompletionSource = null;
        private Predicate<CanMessage> bootupFilter = null;

        private TaskCompletionSource<CanMessage> sdoCompletionSource = null;
        private Predicate<CanMessage> sdoFilter = null;

        public bool IsSegmentedTransfer { get; private set; } = false;


        #region Handles
        static List<ushort> Handles = new List<ushort>()
        {
            PCANBasic.PCAN_ISABUS1,
            PCANBasic.PCAN_ISABUS2,
            PCANBasic.PCAN_ISABUS3,
            PCANBasic.PCAN_ISABUS4,
            PCANBasic.PCAN_ISABUS5,
            PCANBasic.PCAN_ISABUS6,
            PCANBasic.PCAN_ISABUS7,
            PCANBasic.PCAN_ISABUS8,
            PCANBasic.PCAN_DNGBUS1,
            PCANBasic.PCAN_PCIBUS1,
            PCANBasic.PCAN_PCIBUS2,
            PCANBasic.PCAN_PCIBUS3,
            PCANBasic.PCAN_PCIBUS4,
            PCANBasic.PCAN_PCIBUS5,
            PCANBasic.PCAN_PCIBUS6,
            PCANBasic.PCAN_PCIBUS7,
            PCANBasic.PCAN_PCIBUS8,
            PCANBasic.PCAN_PCIBUS9,
            PCANBasic.PCAN_PCIBUS10,
            PCANBasic.PCAN_PCIBUS11,
            PCANBasic.PCAN_PCIBUS12,
            PCANBasic.PCAN_PCIBUS13,
            PCANBasic.PCAN_PCIBUS14,
            PCANBasic.PCAN_PCIBUS15,
            PCANBasic.PCAN_PCIBUS16,
            PCANBasic.PCAN_USBBUS1,
            PCANBasic.PCAN_USBBUS2,
            PCANBasic.PCAN_USBBUS3,
            PCANBasic.PCAN_USBBUS4,
            PCANBasic.PCAN_USBBUS5,
            PCANBasic.PCAN_USBBUS6,
            PCANBasic.PCAN_USBBUS7,
            PCANBasic.PCAN_USBBUS8,
            PCANBasic.PCAN_USBBUS9,
            PCANBasic.PCAN_USBBUS10,
            PCANBasic.PCAN_USBBUS11,
            PCANBasic.PCAN_USBBUS12,
            PCANBasic.PCAN_USBBUS13,
            PCANBasic.PCAN_USBBUS14,
            PCANBasic.PCAN_USBBUS15,
            PCANBasic.PCAN_USBBUS16,
            PCANBasic.PCAN_PCCBUS1,
            PCANBasic.PCAN_PCCBUS2,
            PCANBasic.PCAN_LANBUS1,
            PCANBasic.PCAN_LANBUS2,
            PCANBasic.PCAN_LANBUS3,
            PCANBasic.PCAN_LANBUS4,
            PCANBasic.PCAN_LANBUS5,
            PCANBasic.PCAN_LANBUS6,
            PCANBasic.PCAN_LANBUS7,
            PCANBasic.PCAN_LANBUS8,
            PCANBasic.PCAN_LANBUS9,
            PCANBasic.PCAN_LANBUS10,
            PCANBasic.PCAN_LANBUS11,
            PCANBasic.PCAN_LANBUS12,
            PCANBasic.PCAN_LANBUS13,
            PCANBasic.PCAN_LANBUS14,
            PCANBasic.PCAN_LANBUS15,
            PCANBasic.PCAN_LANBUS16,
        };
        #endregion

        #region Constructors
        #endregion

        #region Methods
        public ushort FindAdapter() => FindAllAdapters().FirstOrDefault();
        public IEnumerable<ushort> FindAllAdapters()
        {
            foreach (var handle in Handles)
            {
                if (handle <= PCANBasic.PCAN_PCIBUS1) //non-pnp
                    continue;

                var status = PCANBasic.GetValue(handle, TPCANParameter.PCAN_CHANNEL_CONDITION, out uint value, sizeof(uint));
                if ((status == TPCANStatus.PCAN_ERROR_OK) && ((value & PCANBasic.PCAN_CHANNEL_AVAILABLE) == PCANBasic.PCAN_CHANNEL_AVAILABLE))
                    yield return handle;
            }
        }
        public IEnumerable<KeyValuePair<ushort, string>> FindAllAdaptersDescriptive()
        {
            foreach (var handle in Handles)
            {
                if (handle <= PCANBasic.PCAN_PCIBUS1) //non-pnp
                    continue;

                var status = PCANBasic.GetValue(handle, TPCANParameter.PCAN_CHANNEL_CONDITION, out uint value, sizeof(uint));
                if ((status == TPCANStatus.PCAN_ERROR_OK) && ((value & PCANBasic.PCAN_CHANNEL_AVAILABLE) == PCANBasic.PCAN_CHANNEL_AVAILABLE))
                {
                    TPCANDevice deviceType;
                    byte channel;

                    if (handle < 0x100)
                    {
                        deviceType = (TPCANDevice)(handle >> 4);
                        channel = (byte)(handle & 0xF);
                    }
                    else
                    {
                        deviceType = (TPCANDevice)(handle >> 8);
                        channel = (byte)(handle & 0xFF);
                    }

                    yield return new KeyValuePair<ushort, string>(handle, $"{deviceType.ToString().Replace("_", "-")} {channel} [{handle:X2}h]");
                }
            }
        }

        public void Connect(ushort handle, RoboControllerBaudRate baudRate, byte node)
        {
            if (currentHandle == handle)
                return;

            if (currentHandle != 0)
                throw new RoboException(RoboExceptionCode.ErrorAlreadyConnected, "Another device is already connected.");

            var status = PCANBasic.Initialize(handle, (TPCANBaudrate) baudRate);
            if (status != TPCANStatus.PCAN_ERROR_OK)
                throw new RoboException(RoboExceptionCode.PCANErrorInitializing, status);

            //string traceFilePath = Path.Combine(Path.GetDirectoryName(Application.ExecutablePath), "logs");
            //status = PCANBasic.SetValue(handle, TPCANParameter.PCAN_TRACE_LOCATION, traceFilePath, (uint)traceFilePath.Length);

            //uint parameterTraceOptions = PCANBasic.TRACE_FILE_OVERWRITE | PCANBasic.TRACE_FILE_SEGMENTED;
            //status = PCANBasic.SetValue(handle, TPCANParameter.PCAN_TRACE_CONFIGURE, ref parameterTraceOptions, sizeof(uint));

            //var parameterOn = (uint)PCANBasic.PCAN_PARAMETER_ON;
            //status = PCANBasic.SetValue(handle, TPCANParameter.PCAN_TRACE_STATUS, ref parameterOn, sizeof(UInt32));

            var receiveEvent = new AutoResetEvent(false);
            var receiveEventHandle = Convert.ToUInt32(receiveEvent.SafeWaitHandle.DangerousGetHandle().ToInt32());
            status = PCANBasic.SetValue(handle, TPCANParameter.PCAN_RECEIVE_EVENT, ref receiveEventHandle, sizeof(UInt32));
            if (status != TPCANStatus.PCAN_ERROR_OK)
            {
                PCANBasic.Uninitialize(handle);
                throw new RoboException(RoboExceptionCode.PCANErrorRegisterHandler, "Could not register read event handler.");
            }

            listenerCancellationSource = new CancellationTokenSource();
            var cancellationToken = listenerCancellationSource.Token;

            Task.Factory.StartNew(() =>
            {
                try
                {
                    Listen(handle, receiveEvent, cancellationToken);
                }
                catch (OperationCanceledException) //disconnect
                {
                }
                catch (Exception) //this should not be reached.
                {
                }
            }, TaskCreationOptions.LongRunning);

            currentNode = node;
            currentHandle = handle;
            currentBaudRate = baudRate;
        }
        public void Disconnect()
        {
            listenerCancellationSource?.Cancel();

            if (currentHandle != 0)
                PCANBasic.Uninitialize(currentHandle);

            currentHandle = 0;
        }

        protected void OnMessageComposed(MessageEventArgs args)
        {
            MessageComposed?.Invoke(this, args);
        }
        protected void OnMessageReceived(MessageEventArgs args)
        {
            MessageReceived?.Invoke(this, args);
        }

        protected void Listen(ushort handle, AutoResetEvent receiveEvent, CancellationToken cancellationToken)
        {
            ulong? prevTime = null;
            while (true)
            {
                cancellationToken.ThrowIfCancellationRequested();

                if (receiveEvent.WaitOne(20))
                {
                    while (PCANBasic.Read(handle, out var pcanMessage, out var timestamp) == TPCANStatus.PCAN_ERROR_OK)
                    {
                        var newTimestamp = timestamp.micros + 1000UL * timestamp.millis + 0x100000000UL * 1000UL * timestamp.millis_overflow;
                        prevTime = prevTime ?? newTimestamp;
                        newTimestamp -= prevTime.Value;

                        var message = new CanMessage(newTimestamp, (CanMessageType)pcanMessage.MSGTYPE, pcanMessage.ID, pcanMessage.LEN, pcanMessage.DATA);

                        try { OnMessageReceived(new MessageEventArgs(message.ID, message.Length, message.Data)); }
                        catch { }

                        try
                        {

                            if (sdoFilter != null)
                                ProcessSdo(message);

                            if (bootupFilter != null)
                                ProcessBootup(message);
                        }
                        finally
                        {
                        }
                    }
                }
            }
        }
        protected void ProcessBootup(CanMessage message)
        {
            if (bootupFilter?.Invoke(message) ?? false)
                bootupCompletionSource?.TrySetResult(message);
        }
        protected void ProcessSdo(CanMessage message)
        {
            if (sdoFilter?.Invoke(message) ?? false)
                sdoCompletionSource?.TrySetResult(message);
        }

        protected Predicate<CanMessage> GetSdoFilter(byte node, uint index, byte subIndex)
        {
            return (m) => m.ID == 0x580 + node
                && m.Length >= 4
                && m.Data[1] == (byte)(index & 0xFF)
                && m.Data[2] == (byte)((index >> 8) & 0xFF)
                && m.Data[3] == subIndex;
        }
        protected Predicate<CanMessage> GetSdoFilter(byte node) => (m) => m.ID == 0x580 + node;
        protected void CreateSdoCompletionSource(Predicate<CanMessage> filter)
        {
            sdoFilter = null;
            sdoCompletionSource = new TaskCompletionSource<CanMessage>();
            sdoFilter = filter;
        }
        protected void ClearSdoCompletionSource()
        {
            sdoFilter = null;
            sdoCompletionSource = null;
        }

        protected bool Write(uint canID, byte[] data, int len)
        {
            var msg = new TPCANMsg
            {
                ID = canID,
                LEN = (byte)Math.Min(len, 8),
                DATA = new byte[8]
            };

            for (int i = 0; i < msg.LEN; i++)
            {
                msg.DATA[i] = data[i];
            }

            if (currentHandle == 0)
                return false;

            var result = PCANBasic.Write(currentHandle, ref msg) == TPCANStatus.PCAN_ERROR_OK;

            try { OnMessageComposed(new MessageEventArgs(msg.ID, msg.LEN, msg.DATA)); }
            catch { }

            return result;
        }
        public bool Write(uint canID, byte[] data) => Write(canID, data, data.Length);
        protected bool WriteSdo(byte node, byte commandByte, ushort index, byte subIndex, byte[] data)
        {
            if (currentHandle == 0)
                return false;

            var msg = new TPCANMsg
            {
                ID = 0x600U + node,
                LEN = (byte)(4 + Math.Min(data.Length, 4)),
                DATA = new byte[8]
            };

            msg.DATA[0] = commandByte;
            msg.DATA[1] = (byte)(index & 0xFF);
            msg.DATA[2] = (byte)((index >> 8) & 0xFF);
            msg.DATA[3] = subIndex;

            for (int i = 4; i < msg.LEN; i++)
            {
                msg.DATA[i] = data[i - 4];
            }

            var result = PCANBasic.Write(currentHandle, ref msg) == TPCANStatus.PCAN_ERROR_OK;

            try { OnMessageComposed(new MessageEventArgs(msg.ID, msg.LEN, msg.DATA)); }
            catch { }

            return result;

        }
        protected bool WriteSdo(byte node, byte commandByte, ushort index, byte subIndex) => WriteSdo(node, commandByte, index, subIndex, new byte[] { });

        protected byte[] ReadObject(TimeSpan timeout, byte node, ushort index, byte subIndex)
        {
            try
            {
                CreateSdoCompletionSource(GetSdoFilter(node, index, subIndex));

                if (!WriteSdo(node, 0x40, index, subIndex))
                    return null;

                if (!sdoCompletionSource.Task.Wait(timeout))
                    return null;

                var message = sdoCompletionSource.Task.Result;
                var commandByte = message.Data[0];
                ClearSdoCompletionSource();

                if ((commandByte & 0x80) != 0) //abort transmission
                    return null;

                if ((commandByte & 0xE0) != 0x40) //read response
                    return null;

                if ((commandByte & 0x03) == 0x03) //expedited with length indication
                    return message.Data.Skip(4).Take(4 - ((commandByte & 0x0C) >> 2)).Reverse().ToArray();

                //segmented transfer
                if ((commandByte & 0x03) != 0x01)
                    return null;

                IsSegmentedTransfer = true;

                var list = new List<byte>(); //we can use size in this message to reserve buffer
                byte requestByte = 0x70;
                byte responseByte = 0x10;
                while (true)
                {
                    CreateSdoCompletionSource(GetSdoFilter(node));

                    requestByte ^= 0x10;
                    responseByte ^= 0x10;

                    if (!WriteSdo(node, requestByte, index, subIndex))
                        return null;

                    if (!sdoCompletionSource.Task.Wait(timeout))
                        return null;

                    message = sdoCompletionSource.Task.Result;
                    ClearSdoCompletionSource();

                    if (message.Length < 2)
                        return null;

                    commandByte = message.Data[0];
                    if ((commandByte & 0xF0) != responseByte)
                        return null;

                    list.AddRange(message.Data.Skip(1).Take(7 - ((commandByte & 0x0E) >> 1)).ToArray());

                    //last segment
                    if ((commandByte & 0x01) == 0x01)
                        break;
                }

                return list.ToArray();
            }
            finally
            {
                ClearSdoCompletionSource();
                IsSegmentedTransfer = false;
            }
        }
        protected bool WriteObject(TimeSpan timeout, byte node, ushort index, byte subIndex, byte[] data, CancellationToken cancellationToken = default, IProgress<int> progress = null)
        {
            if (data.Length == 0)
                return false;

            var nodeFilter = GetSdoFilter(node);

            try
            {
                var isSegmented = data.Length > 4;

                CreateSdoCompletionSource(GetSdoFilter(node, index, subIndex));
                if (isSegmented)
                {
                    if (!WriteSdo(node, 0x21, index, subIndex, BitConverter.GetBytes((uint)data.Length).ToArray()))
                        return false;
                }
                else
                {
                    if (!WriteSdo(node, (byte)(0x23 | ((4 - data.Length) << 2)), index, subIndex, data))
                        return false;
                }

                if (!sdoCompletionSource.Task.Wait(Convert.ToInt32(timeout.TotalMilliseconds), cancellationToken))
                    return false;

                var message = sdoCompletionSource.Task.Result;
                var commandByte = message.Data[0];

                ClearSdoCompletionSource();

                if ((commandByte & 0xE0) != 0x60) //write confirm
                    return false;

                if (!isSegmented)
                    return true;

                IsSegmentedTransfer = true;

                var lastPercent = 0;
                progress?.Report(0);

                byte requestByte = 0x10;
                byte responseByte = 0x30;
                for (int i = 0; i < data.Length; i += 7)
                {
                    requestByte ^= 0x10;
                    responseByte ^= 0x10;

                    var len = (byte)Math.Min(7, data.Length - i);
                    var options = (byte)(((data.Length > i + 7) ? 0 : 1) | ((7 - len) << 1));

                    var arr = new byte[] { (byte)(requestByte | options) }.Concat(data.Skip(i).Take(len)).ToArray();

                    CreateSdoCompletionSource(nodeFilter);
                    if (!Write(0x600U + node, arr))
                        return false;

                    if (!sdoCompletionSource.Task.Wait(Convert.ToInt32(timeout.TotalMilliseconds), cancellationToken))
                        return false;

                    message = sdoCompletionSource.Task.Result;
                    ClearSdoCompletionSource();

                    if (message.Length < 2 || (message.Data[0] & 0xF0) != responseByte)
                        return false;

                    var percent = 100 * (i + 7) / data.Length;

                    if (percent > 100)
                        percent = 100;

                    if (percent != lastPercent)
                        progress?.Report(percent);

                    lastPercent = percent;
                }

                return true;
            }
            finally
            {
                ClearSdoCompletionSource();
                IsSegmentedTransfer = false;
            }
        }

        private byte[] GetBytesLittleEndian(int value)
        {
            byte[] b = new byte[4];
            b[0] = (byte)value;
            b[1] = (byte)((value >> 8) & 0xFF);
            b[2] = (byte)((value >> 16) & 0xFF);
            b[3] = (byte)((value >> 24) & 0xFF);

            return b;
        }
        public int? ReadObjectS32(TimeSpan timeout, byte node, ushort index, byte subIndex)
        {
            var result = ReadObject(timeout, node, index, subIndex);
            if (result == null || result.Length == 0 || result.Length > 4)
                return null;

            int value = 0;
            for (int i = 0; i < result.Length; i++)
            {
                value <<= 8;
                value |= result[i];
            }

            return value;
        }
        public bool WriteObjectS32(byte node, ushort index, byte subIndex, int value) => WriteObject(SdoTimeout, node, index, subIndex, GetBytesLittleEndian(value));
        #endregion

        #region Controller Methods
        protected bool IsNumericType(RoboCommandDataType type)
        {
            switch (type)
            {
                case RoboCommandDataType.TYPE_ID_U8:
                case RoboCommandDataType.TYPE_ID_S8:
                case RoboCommandDataType.TYPE_ID_U16:
                case RoboCommandDataType.TYPE_ID_S16:
                case RoboCommandDataType.TYPE_ID_U32:
                case RoboCommandDataType.TYPE_ID_S32:
                case RoboCommandDataType.TYPE_ID_B32:
                case RoboCommandDataType.SIZEM:
                    return true;
            }

            return false;
        }
        protected byte[] ToByteArray(RoboCommand command, int value)
        {
            int valueSize;
            switch (command.DataType)
            {
                case RoboCommandDataType.TYPE_ID_U8:
                case RoboCommandDataType.TYPE_ID_S8:
                    valueSize = 1;
                    break;

                case RoboCommandDataType.TYPE_ID_U16:
                case RoboCommandDataType.TYPE_ID_S16:
                    valueSize = 2;
                    break;

                case RoboCommandDataType.TYPE_ID_U32:
                case RoboCommandDataType.TYPE_ID_S32:
                case RoboCommandDataType.TYPE_ID_B32:
                    valueSize = 4;
                    break;

                default:
                    throw new RoboException(RoboExceptionCode.ErrorCommandNotNumeric, $"'{command.Name}[{command.DataType}]' isn't of a numeric type.");
            }

            return Enumerable.Range(0, valueSize).Select(i => (byte)((value >> (i * 8)) & 0xFF)).ToArray();
        }
        public void SetCommand(string commandName, int commandIndex, int value)
        {
            var command = RoboCommandHelper.GetCommand(commandName);
            if (command == null)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotFound, $"Could not find command '{commandName}'.");

            command.GetCanOpenObject(commandIndex, out var canopenIndex, out var canopenSubIndex);

            if (command.AccessType != RoboCommandAccessType.WriteOnly && command.AccessType != RoboCommandAccessType.ReadWrite)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotWritable, $"Command '{commandName}' is not writable.");

            var arr = ToByteArray(command, value);
            if (!WriteObject(SdoTimeout, currentNode, (ushort)canopenIndex, (byte)canopenSubIndex, arr))
                throw new RoboException(RoboExceptionCode.ErrorGettingConfig, $"Writing command '!{commandName} {commandIndex} {value}' failed.");
        }
        public int GetValue(string commandName, int commandIndex)
        {
            var command = RoboCommandHelper.GetQuery(commandName);
            if (command == null)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotFound, $"Could not find query '{commandName}'.");

            command.GetCanOpenObject(commandIndex, out var canopenIndex, out var canopenSubIndex);

            if (command.AccessType != RoboCommandAccessType.ReadOnly && command.AccessType != RoboCommandAccessType.ReadWrite)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotReadable, $"Query '{commandName}' is not readable.");

            if (!IsNumericType(command.DataType))
                throw new RoboException(RoboExceptionCode.ErrorCommandNotNumeric, $"Query '{commandName}' doesn't return a numeric value.");

            var result = ReadObjectS32(SdoTimeout, currentNode, (ushort)canopenIndex, (byte)canopenSubIndex);
            if (result == null)
                throw new RoboException(RoboExceptionCode.ErrorGettingConfig, $"Reading query '?{commandName} {commandIndex}' failed.");

            return result.Value;
        }
        public string GetValueString(string commandName, int commandIndex)
        {
            var command = RoboCommandHelper.GetQuery(commandName);
            if (command == null)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotFound, $"Could not find query '{commandName}'.");

            command.GetCanOpenObject(commandIndex, out var canopenIndex, out var canopenSubIndex);

            if (command.AccessType != RoboCommandAccessType.ReadOnly && command.AccessType != RoboCommandAccessType.ReadWrite)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotReadable, $"Query '{commandName}' is not readable.");

            if (command.DataType != RoboCommandDataType.TYPE_ID_STRING)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotString, $"Query '{commandName}' doesn't return a string value.");

            var result = ReadObject(SdoTimeout, currentNode, (ushort)canopenIndex, (byte)canopenSubIndex);
            if (result == null)
                throw new RoboException(RoboExceptionCode.ErrorGettingConfig, $"Reading query '?{commandName} {commandIndex}' failed.");

            return Encoding.UTF8.GetString(result);
        }
        public void SetConfig(string commandName, int commandIndex, int value)
        {
            var command = RoboCommandHelper.GetConfig(commandName);
            if (command == null)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotFound, $"Could not find configuration '{commandName}'.");

            command.GetCanOpenObject(commandIndex, out var canopenIndex, out var canopenSubIndex);

            if (command.AccessType != RoboCommandAccessType.WriteOnly && command.AccessType != RoboCommandAccessType.ReadWrite)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotWritable, $"Configuration '{commandName}' is not writable.");

            var arr = ToByteArray(command, value);
            if (!WriteObject(SdoTimeout, currentNode, (ushort)canopenIndex, (byte)canopenSubIndex, arr))
                throw new RoboException(RoboExceptionCode.ErrorGettingConfig, $"Writing configuration '^{commandName} {commandIndex} {value}' failed.");
        }
        public int GetConfig(string commandName, int commandIndex)
        {
            var command = RoboCommandHelper.GetConfig(commandName);
            if (command == null)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotFound, $"Could not find configuration '{commandName}'.");

            command.GetCanOpenObject(commandIndex, out var canopenIndex, out var canopenSubIndex);

            if (command.AccessType != RoboCommandAccessType.ReadOnly && command.AccessType != RoboCommandAccessType.ReadWrite)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotReadable, $"Configuration '{commandName}' is not readable.");

            if (!IsNumericType(command.DataType))
                throw new RoboException(RoboExceptionCode.ErrorCommandNotNumeric, $"Configuration '{commandName}' doesn't return a numeric value.");

            var result = ReadObjectS32(SdoTimeout, currentNode, (ushort)canopenIndex, (byte)canopenSubIndex);
            if (result == null)
                throw new RoboException(RoboExceptionCode.ErrorGettingConfig, $"Reading configuration '~{commandName} {commandIndex}' failed.");

            return result.Value;
        }
        public void SetMaintenance(string commandName, int commandIndex, int value)
        {
            var command = RoboCommandHelper.GetMaintenance(commandName);
            if (command == null)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotFound, $"Could not find maintenance '{commandName}'.");

            command.GetCanOpenObject(commandIndex, out var canopenIndex, out var canopenSubIndex);

            if (command.AccessType != RoboCommandAccessType.WriteOnly && command.AccessType != RoboCommandAccessType.ReadWrite)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotWritable, $"Maintenance '{commandName}' is not writable.");

            var arr = ToByteArray(command, value);
            if (!WriteObject(SdoTimeout, currentNode, (ushort)canopenIndex, (byte)canopenSubIndex, arr))
                throw new RoboException(RoboExceptionCode.ErrorGettingConfig, $"Executing maintenance command '%{commandName} {commandIndex} {value}' failed.");
        }
        public void SetMaintenanceString(string commandName, int commandIndex, string value)
        {
            var command = RoboCommandHelper.GetMaintenance(commandName);
            if (command == null)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotFound, $"Could not find maintenance '{commandName}'.");

            command.GetCanOpenObject(commandIndex, out var canopenIndex, out var canopenSubIndex);

            if (command.AccessType != RoboCommandAccessType.WriteOnly && command.AccessType != RoboCommandAccessType.ReadWrite)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotWritable, $"Maintenance '{commandName}' is not writable.");

            if (command.DataType != RoboCommandDataType.TYPE_ID_STRING)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotString, $"Maintenance '{commandName}' doesn't accept string value.");

            var arr = Encoding.UTF8.GetBytes(value);
            if (!WriteObject(SdoTimeout, currentNode, (ushort)canopenIndex, (byte)canopenSubIndex, arr))
                throw new RoboException(RoboExceptionCode.ErrorGettingConfig, $"Executing maintenance command '%{commandName} {commandIndex} {value}' failed.");
        }
        public string GetMaintenanceString(string commandName, int commandIndex)
        {
            var command = RoboCommandHelper.GetMaintenance(commandName);
            if (command == null)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotFound, $"Could not find maintenance '{commandName}'.");

            command.GetCanOpenObject(commandIndex, out var canopenIndex, out var canopenSubIndex);

            if (command.AccessType != RoboCommandAccessType.ReadOnly && command.AccessType != RoboCommandAccessType.ReadWrite)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotReadable, $"Maintenance '{commandName}' is not readable.");

            if (command.DataType != RoboCommandDataType.TYPE_ID_STRING)
                throw new RoboException(RoboExceptionCode.ErrorCommandNotString, $"Maintenance '{commandName}' doesn't return a string value.");

            var result = ReadObject(SdoTimeout, currentNode, (ushort)canopenIndex, (byte)canopenSubIndex);
            if (result == null)
                throw new RoboException(RoboExceptionCode.ErrorGettingConfig, $"Reading maintenance '?{commandName} {commandIndex}' failed.");

            return Encoding.UTF8.GetString(result);
        }
        #endregion
    }

    public enum CanMessageType
    {
        /// <summary>
        /// The PCAN message is a CAN Standard Frame (11-bit identifier)
        /// </summary>
        Standard = 0x00,
        /// <summary>
        /// The PCAN message is a CAN Remote-Transfer-Request Frame
        /// </summary>
        RTR = 0x01,
        /// <summary>
        /// The PCAN message is a CAN Extended Frame (29-bit identifier)
        /// </summary>
        Extended = 0x02,
        /// <summary>
        /// The PCAN message represents a FD frame in terms of CiA Specs
        /// </summary>
        FD = 0x04,
        /// <summary>
        /// The PCAN message represents a FD bit rate switch (CAN data at a higher bit rate)
        /// </summary>
        BRS = 0x08,
        /// <summary>
        /// The PCAN message represents a FD error state indicator(CAN FD transmitter was error active)
        /// </summary>
        ESI = 0x10,
        /// <summary>
        /// The PCAN message represents an error frame
        /// </summary>
        Error = 0x40,
        /// <summary>
        /// The PCAN message represents a PCAN status message
        /// </summary>
        Status = 0x80,
    }
    public class CanMessage
    {
        public ulong Microseconds { get; }
        public CanMessageType Type { get; }
        public uint ID { get; }
        public byte Length { get; }
        public byte[] Data { get; } = new byte[] { 0, 0, 0, 0, 0, 0, 0, 0 };

        public CanMessage(ulong microseconds, CanMessageType type, uint id, byte length, byte[] data)
        {
            Microseconds = microseconds;
            Type = type;
            ID = id;
            Length = length;

            for (int i = 0; i < length; i++)
            {
                Data[i] = data[i];
            }
        }

        public string ToLogString()
        {
            var sb = new StringBuilder($"{(Microseconds / 1000.0):F1}\t{ID:X3}\t{Length}\t");
            for (int i = 0; i < Length; i++)
            {
                sb.Append($"{Data[i]:X2} ");
            }

            return sb.ToString();
        }
    }
    public class MessageEventArgs : EventArgs
    {
        public uint ID { get; }
        public byte Length { get; }
        public byte[] Data { get; }

        public MessageEventArgs(uint id, byte length, byte[] data)
        {
            ID = id;
            Length = length;
            Data = data;
        }
    }
}
