using Roboteq.CommandsConfigurator.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace Roboteq.CommandsConfigurator.Helpers
{
    public static class RoboCommandHelper
    {
        static Dictionary<string, RoboCommand> dictCommandMapping = new Dictionary<string, RoboCommand>(StringComparer.InvariantCultureIgnoreCase);
        static Dictionary<int, RoboCommand> dictCommandIndexMapping = new Dictionary<int, RoboCommand>();
        static Dictionary<string, RoboCommand> dictQueryMapping = new Dictionary<string, RoboCommand>(StringComparer.InvariantCultureIgnoreCase);
        static Dictionary<int, RoboCommand> dictQueryIndexMapping = new Dictionary<int, RoboCommand>();
        static Dictionary<string, RoboCommand> dictConfigMapping = new Dictionary<string, RoboCommand>(StringComparer.InvariantCultureIgnoreCase);
        static Dictionary<int, RoboCommand> dictConfigIndexMapping = new Dictionary<int, RoboCommand>();
        static Dictionary<string, RoboCommand> dictMaintenanceMapping = new Dictionary<string, RoboCommand>(StringComparer.InvariantCultureIgnoreCase);
        static Dictionary<int, RoboCommand> dictMaintenanceIndexMapping = new Dictionary<int, RoboCommand>();

        static RoboCommandHelper()
        {
            try
            {
                var fileName = Path.Combine(Path.GetDirectoryName(Assembly.GetAssembly(typeof(RoboCommandHelper)).Location), "Data", "robo-commands.rclx");
                var commandsList = RoboCommandList.Load(fileName);

                AppendToDict(dictCommandMapping, dictCommandIndexMapping, commandsList.Commands);
                AppendToDict(dictQueryMapping, dictQueryIndexMapping, commandsList.Queries);
                AppendToDict(dictConfigMapping, dictConfigIndexMapping, commandsList.Configurations);
                AppendToDict(dictMaintenanceMapping, dictMaintenanceIndexMapping, commandsList.Maintenances);
            }
            catch
            {
            }

        }

        private static void AppendToDict(Dictionary<string, RoboCommand> direct, Dictionary<int, RoboCommand> reverse, IEnumerable<RoboCommand> commands)
        {
            foreach (var item in commands)
            {
                if (!direct.ContainsKey(item.Name))
                    direct[item.Name] = item;

                if (!string.IsNullOrWhiteSpace(item.VerbalName) && !direct.ContainsKey(item.VerbalName))
                    direct[item.VerbalName] = item;

                if (item.CanOpenIndex.HasValue && !reverse.ContainsKey(item.CanOpenIndex.Value))
                    reverse[item.CanOpenIndex.Value] = item;

                if (item.LegacyCanOpenIndex.HasValue && !reverse.ContainsKey(item.LegacyCanOpenIndex.Value))
                    reverse[item.LegacyCanOpenIndex.Value] = item;

                foreach (var index in item.DS402Indices)
                {
                    if (!reverse.ContainsKey(index))
                        reverse[index] = item;
                }
            }
        }

        private static RoboCommand GetCommand(Dictionary<string, RoboCommand> dict, string name) => dict.ContainsKey(name) ? dict[name] : null;
        public static RoboCommand GetCommand(string name) => GetCommand(dictCommandMapping, name);
        public static RoboCommand GetQuery(string name) => GetCommand(dictQueryMapping, name);
        public static RoboCommand GetConfig(string name) => GetCommand(dictConfigMapping, name);
        public static RoboCommand GetMaintenance(string name) => GetCommand(dictMaintenanceMapping, name);

        private static bool FindCanOpenIndex(this RoboCommand command, out int canOpenIndex, out bool isDS402)
        {
            canOpenIndex = 0;
            isDS402 = false;
            if (command.CanOpenIndex.HasValue)
            {
                canOpenIndex = command.CanOpenIndex.Value;
                return true;
            }

            if (command.LegacyCanOpenIndex.HasValue)
            {
                canOpenIndex = command.LegacyCanOpenIndex.Value;
                return true;
            }

            if (command.DS402Indices.Count > 0)
            {
                canOpenIndex = command.DS402Indices.First();
                isDS402 = true;
                return true;
            }

            return false;
        }
        public static void GetCanOpenObject(this RoboCommand command, int? commandIndex, out int canOpenIndex, out int canOpenSubIndex)
        {
            if (!command.Target.HasFlag(RoboCommandTarget.MC))
                throw new ApplicationException($"The '{command.Name}' is not availbale for motor controllers.");

            if (!command.FindCanOpenIndex(out canOpenIndex, out var isDS402))
                throw new ApplicationException($"The '{command.Name}' is not supported in CANOpen.");

            canOpenSubIndex = commandIndex ?? 0;

            if (commandIndex == 0) //No further checks.
                return;

            if(!isDS402)
            {
                if (commandIndex == null && command.VariableSize > 1) //skip number of sub-indices
                    canOpenSubIndex = 1;
            }
            else
            {
                if (commandIndex == null)
                    commandIndex = 1;

                switch (command.DS402Type)
                {
                    case DS402Type.DS402_None:
                    case DS402Type.DS402_MI_SC:
                        break;

                    case DS402Type.DS402_SI_SC:
                        if (commandIndex > 3)
                            throw new ApplicationException($"Unsupported channel '{commandIndex}' for '{command.Name}'.");

                        canOpenSubIndex = 0;
                        break;

                    case DS402Type.DS402_SI_MC:
                    case DS402Type.DS402_2I_MC:
                    case DS402Type.DS402_3I_MC:
                    case DS402Type.DS402_4I_MC:
                    case DS402Type.DS402_5I_MC:
                    case DS402Type.DS402_6I_MC:
                        var numIndices = (int)(command.DS402Type - DS402Type.DS402_SI_MC) + 1;
                        var channel = (commandIndex.Value - 1) / numIndices;

                        if(channel > 2)
                            throw new ApplicationException($"Unsupported channel '{channel + 1}' for '{command.Name}'.");

                        canOpenIndex += channel * 0x800;
                        canOpenSubIndex = ((commandIndex.Value - 1) % numIndices) + 1;

                        if (command.DS402Type == DS402Type.DS402_SI_MC)
                            canOpenSubIndex = 0;

                        break;

                    default:
                        throw new ApplicationException($"Unsupported DS402 type '{command.DS402Type}' for '{command.Name}'.");
                }
            }

            if (canOpenIndex < ushort.MinValue || canOpenIndex > ushort.MaxValue)
                throw new ApplicationException($"Invalid command index range '{commandIndex}' for '{command.Name}'.");

            if (canOpenSubIndex < byte.MinValue || canOpenSubIndex > byte.MaxValue)
                throw new ApplicationException($"Invalid command sub-index range '{commandIndex}' for '{command.Name}'.");
        }
    }
}
