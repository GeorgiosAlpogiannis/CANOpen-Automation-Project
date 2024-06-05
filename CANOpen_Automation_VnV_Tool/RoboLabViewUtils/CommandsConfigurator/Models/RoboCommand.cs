using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;

namespace Roboteq.CommandsConfigurator.Models
{
    [Serializable]
    public class RoboCommand
    {
        public RoboCommandType Category { get; set; }
        public int Code { get; set; }
        public string Name { get; set; }
        [DefaultValue("")]
        public string VerbalName { get; set; }

        public RoboCommandDataType DataType { get; set; } = RoboCommandDataType.UNDEFINED;
        public RoboCommandTarget Target { get; set; } = RoboCommandTarget.None;
        public RoboCommandAccessType AccessType { get; set; } = RoboCommandAccessType.None;

        [DefaultValue(0)]
        public int VariableSize { get; set; } = 0;

        [XmlIgnore]
        public List<string> SupportedVersions { get; set; } = new List<string>();
        [XmlElement(nameof(SupportedVersions))]
        public string SupportedVersionsCSV
        {
            get { return string.Join(",", SupportedVersions); }
            set { SupportedVersions = value.Split(',').ToList(); }
        }

        public int? CanOpenIndex { get; set; } = null;
        public int? LegacyCanOpenIndex { get; set; } = null;

        [XmlIgnore]
        public List<int> DS402Indices { get; set; } = new List<int>();
        [XmlElement(nameof(DS402Indices))]
        public string DS402IndicesCSV
        {
            get { return string.Join(",", DS402Indices); }
            set { DS402Indices = new List<int>(Array.ConvertAll(value.Split(','), int.Parse)); }
        }


        [DefaultValue(DS402Type.DS402_None)]
        public DS402Type DS402Type { get; set; } = DS402Type.DS402_None;
        [DefaultValue(false)]
        public bool AllowPDOMapping { get; set; } = false;

        public bool ShouldSerializeSupportedVersionsCSV() => SupportedVersions.Count > 0;
        public bool ShouldSerializeCanOpenIndex() => CanOpenIndex.HasValue;
        public bool ShouldSerializeLegacyCanOpenIndex() => LegacyCanOpenIndex.HasValue;
        public bool ShouldSerializeDS402IndicesCSV() => DS402Indices.Count > 0;
        public bool ShouldSerializeAllowPDOMapping() => AllowPDOMapping;
    }

    [Serializable]
    public class RoboCommandList
    {
        public string Name { get; set; }
        public string Version { get; set; }
        public DateTime CreationDate { get; set; }
        public string FileFormat { get; set; } = "rclx/v1.0";

        public List<RoboCommand> Commands { get; set; }
        public List<RoboCommand> Queries { get; set; }
        public List<RoboCommand> Configurations { get; set; }
        public List<RoboCommand> Maintenances { get; set; }

        public static RoboCommandList Load(string fileName)
        {
            var serializer = new XmlSerializer(typeof(RoboCommandList));
            using (var stream = File.OpenRead(fileName))
            {
                return serializer.Deserialize(stream) as RoboCommandList;
            }
        }
        public void Save(string fileName)
        {
            var serializer = new XmlSerializer(this.GetType());
            using (var stream = File.Create(fileName))
            {
                serializer.Serialize(stream, this);
            }
        }
    }

    public enum RoboCommandType
    {
        Command,
        Query,
        Configuration,
        Maintenance,
    }
    public enum RoboCommandDataType
    {
        UNDEFINED,
        TYPE_ID_U8,
        TYPE_ID_S8,
        TYPE_ID_U16,
        TYPE_ID_S16,
        TYPE_ID_U32,
        TYPE_ID_S32,
        TYPE_ID_B32,
        SIZEM,
        TYPE_ID_STRING,
        TYPE_ID_MBV,
        TYPE_ID_MBB,
    }
    public enum RoboCommandAccessType
    {
        None,
        ReadOnly,
        WriteOnly,
        ReadWrite,
    }

    [Flags]
    public enum RoboCommandTarget
    {
        None = 0x00,
        MC = 0x01,
        RIOX = 0x02,
        MGS = 0x04,
        OTS = 0x08,
        BMS = 0x10,
        FLW = 0x20
    }

    public enum DS402Type
    {
        [EnumText("")] DS402_None,

        [EnumText("SI SC")] DS402_SI_SC,
        [EnumText("MI MC")] DS402_MI_SC,

        [EnumText("SI MC")] DS402_SI_MC,
        [EnumText("2I MC")] DS402_2I_MC,
        [EnumText("3I MC")] DS402_3I_MC,
        [EnumText("4I MC")] DS402_4I_MC,
        [EnumText("5I MC")] DS402_5I_MC,
        [EnumText("6I MC")] DS402_6I_MC,
    }

    [AttributeUsage(AttributeTargets.Field, Inherited = false, AllowMultiple = false)]
    public sealed class EnumTextAttribute : Attribute
    {
        public string Text { get; }
        public EnumTextAttribute(string text)
        {
            Text = text;
        }
    }
}
