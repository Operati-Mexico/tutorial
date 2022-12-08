using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Google.Apis.Auth.OAuth2;
using Google.Cloud.BigQuery.V2;

namespace ConsoleAppBiqueryData
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string projectId = "info-publica-mem";
            var credentials = GoogleCredential.FromFile("C:/Users/Jesus/Downloads/info-publica-mem-key.json");

            string query = @"SELECT ClavedeNodo, Fecha, Hora, PMLTotal, PMLCongestion, PMLEnergia, PMLPerdidas, TipodeMercado
            FROM `info-publica-mem`.Mercado.PML
            WHERE ClavedeNodo in ( 'ENSENADA','CARMEN') and TipodeMercado in ('MDA','MTR') and 
            fecha BETWEEN '2018-01-01' AND '2021-01-01'";

            var client = BigQueryClient.Create(projectId, credentials);

            var result = client.ExecuteQuery(query, parameters: null);

            Console.Write("\nQuery Results:\n------------\n");
            foreach (var row in result)
            {
                Console.WriteLine($"{row["ClavedeNodo"]}, {row["Fecha"]}, {row["Hora"]}, {row["PMLTotal"]}, {row["PMLCongestion"]}, {row["PMLEnergia"]}, {row["PMLPerdidas"]}, {row["TipodeMercado"]}");
            }

        }
    }
}
