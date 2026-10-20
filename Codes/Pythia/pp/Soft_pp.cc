#include <iostream>
#include "Pythia8/Pythia.h"
#include <string>
#include <filesystem>

using namespace Pythia8;
namespace fs = std::filesystem;

// Boolean function to identify charm hadrons:
bool isCharmHadron(int id)
{
  int idAbs = abs(id);
  if (idAbs >= 411 && idAbs <= 435)
    return true;
  return false;
}

// Função principal
int main(int argc, char *argv[])
{
  if (argc < 2)
  {
    std::cerr << "Uso: " << argv[0] << "<ecm_em_GeV>" << std::endl;
  }

  std::string eCM_str = argv[1];
  Pythia pythia;

  pythia.readString("Beams:idA = 2212");       // proton
  pythia.readString("Beams:idB = 2212"); // proton
  pythia.readString("Beams:eCM = " + eCM_str);


  pythia.readString("SoftQCD:all = on");
  // pythia.readString("HardQCD:all = on");

  pythia.readString("HadronLevel:all = on");

  // pythia.readString("HardQCD:hardccbar = on");
  // pythia.readString("HardQCD:gg2ccbar = on");
  // pythia.readString("HardQCD:qqbar2ccbar = on");

  pythia.readString("411:mayDecay = off");  // D+
  pythia.readString("-411:mayDecay = off"); // D-
  pythia.readString("421:mayDecay = off");  // D0
  pythia.readString("-421:mayDecay = off"); // D0bar
  pythia.readString("413:mayDecay = off");  // D*+
  pythia.readString("-413:mayDecay = off"); // D*-
  pythia.readString("423:mayDecay = off");  // D*0
  pythia.readString("-423:mayDecay = off"); // D*0bar
  pythia.readString("415:mayDecay = off");  // D2*+
  pythia.readString("-415:mayDecay = off"); // D2*-
  pythia.readString("425:mayDecay = off");  // D2*0
  pythia.readString("-425:mayDecay = off"); // D2*0bar
  pythia.readString("431:mayDecay = off");  // Ds+
  pythia.readString("-431:mayDecay = off"); // Ds-
  pythia.readString("433:mayDecay = off");  // Ds*+
  pythia.readString("-433:mayDecay = off"); // Ds*-
  pythia.readString("435:mayDecay = off");  // Ds2*
  pythia.readString("-435:mayDecay = off"); // Ds2*bar

  if (!pythia.init())
  {
    cout << "Erro: falha na inicialização do Pythia." << endl;
    return 1;
  }
  cout << "Pythia inicializado com sucesso." << endl;

  // =========================================================================
  // 1. HISTOGRAMAS DE MULTIPLICIDADE POR EVENTO P(N)
  // 9 faixas de eta (0-7 e Asym) para os 3 cenários de pT
  // =========================================================================
  Hist mult_charm_global[9], mult_charm_pt5[9], mult_charm_pt10[9];
  Hist mult_parton_global[9], mult_parton_pt5[9], mult_parton_pt10[9];
  Hist mult_dmeson_global[9], mult_dmeson_pt5[9], mult_dmeson_pt10[9];

  // =========================================================================
  // 2. HISTOGRAMAS DE dN/deta (Distribuição diferencial)
  // =========================================================================
  Hist dNeta_charm_global[9], dNeta_charm_pt5[9], dNeta_charm_pt10[9];
  Hist dNeta_parton_global[9], dNeta_parton_pt5[9], dNeta_parton_pt10[9];
  Hist dNeta_dmeson_global[9], dNeta_dmeson_pt5[9], dNeta_dmeson_pt10[9];

  for (int i = 0; i < 9; ++i)
  {
    // Multiplicidade (eixo X de 0 a 100 partículas por evento)
    mult_charm_global[i] = Hist(" ", 100, -0.5, 99.5);
    mult_charm_pt5[i] = Hist(" ", 100, -0.5, 99.5);
    mult_charm_pt10[i] = Hist(" ", 100, -0.5, 99.5);

    mult_parton_global[i] = Hist(" ", 100, -0.5, 99.5);
    mult_parton_pt5[i] = Hist(" ", 100, -0.5, 99.5);
    mult_parton_pt10[i] = Hist(" ", 100, -0.5, 99.5);

    mult_dmeson_global[i] = Hist(" ", 100, -0.5, 99.5);
    mult_dmeson_pt5[i] = Hist(" ", 100, -0.5, 99.5);
    mult_dmeson_pt10[i] = Hist(" ", 100, -0.5, 99.5);

    // dN/deta (eixo X de rapidez de -10 a 10)
    dNeta_charm_global[i] = Hist(" ", 100, -10.0, 10.0);
    dNeta_charm_pt5[i] = Hist(" ", 100, -10.0, 10.0);
    dNeta_charm_pt10[i] = Hist(" ", 100, -10.0, 10.0);

    dNeta_parton_global[i] = Hist(" ", 100, -10.0, 10.0);
    dNeta_parton_pt5[i] = Hist(" ", 100, -10.0, 10.0);
    dNeta_parton_pt10[i] = Hist(" ", 100, -10.0, 10.0);

    dNeta_dmeson_global[i] = Hist(" ", 100, -10.0, 10.0);
    dNeta_dmeson_pt5[i] = Hist(" ", 100, -10.0, 10.0);
    dNeta_dmeson_pt10[i] = Hist(" ", 100, -10.0, 10.0);
  }

  int nEvent = 10000; // 1000000;
  int nAcceptedEvents = 0;

  for (int iEvent = 0; iEvent < nEvent; ++iEvent)
  {
    if (!pythia.next())
      continue;

    nAcceptedEvents++;

    // Contadores temporários por evento para multiplicidade
    int n_charm_glob[9] = {0}, n_charm_pt5[9] = {0}, n_charm_pt10[9] = {0};
    int n_parton_glob[9] = {0}, n_parton_pt5[9] = {0}, n_parton_pt10[9] = {0};
    int n_dmeson_glob[9] = {0}, n_dmeson_pt5[9] = {0}, n_dmeson_pt10[9] = {0};

    for (int i = 0; i < pythia.event.size(); ++i)
    {
      double eta = pythia.event[i].eta();
      double pT = pythia.event[i].pT();

      // Condições de rapidez (0 a 7 e Asym)
      bool in_eta[9];
      in_eta[0] = (fabs(eta) < 0.5);
      in_eta[1] = (fabs(eta) < 1.0);
      in_eta[2] = (fabs(eta) < 2.0);
      in_eta[3] = (fabs(eta) < 3.0);
      in_eta[4] = (fabs(eta) < 4.0);
      in_eta[5] = (fabs(eta) < 5.0);
      in_eta[6] = (fabs(eta) < 6.0);
      in_eta[7] = (fabs(eta) < 7.0);
      in_eta[8] = (eta > -3.1 && eta < 5.0); // Asym (ajuste se necessário para -3.1 a 5.0)

      // --- 1. Charm Total ---
      if (abs(pythia.event[i].id()) == 4)
      {
        for (int idx = 0; idx < 9; ++idx)
        {
          if (in_eta[idx])
          {
            n_charm_glob[idx]++;
            if (pT > 5.0)
              n_charm_pt5[idx]++;
            if (pT > 10.0)
              n_charm_pt10[idx]++;

            // Preenche dN/deta diretamente por partícula
            dNeta_charm_global[idx].fill(eta);
            if (pT > 5.0)
              dNeta_charm_pt5[idx].fill(eta);
            if (pT > 10.0)
              dNeta_charm_pt10[idx].fill(eta);
          }
        }
      }

      // --- 2. Final Parton Level Charm ---
      if (pythia.event[i].isFinalPartonLevel() && abs(pythia.event[i].id()) == 4)
      {
        for (int idx = 0; idx < 9; ++idx)
        {
          if (in_eta[idx])
          {
            n_parton_glob[idx]++;
            if (pT > 5.0)
              n_parton_pt5[idx]++;
            if (pT > 10.0)
              n_parton_pt10[idx]++;

            dNeta_parton_global[idx].fill(eta);
            if (pT > 5.0)
              dNeta_parton_pt5[idx].fill(eta);
            if (pT > 10.0)
              dNeta_parton_pt10[idx].fill(eta);
          }
        }
      }

      // --- 3. D Mesons ---
      if (pythia.event[i].isFinal() && isCharmHadron(pythia.event[i].id()))
      {
        for (int idx = 0; idx < 9; ++idx)
        {
          if (in_eta[idx])
          {
            n_dmeson_glob[idx]++;
            if (pT > 5.0)
              n_dmeson_pt5[idx]++;
            if (pT > 10.0)
              n_dmeson_pt10[idx]++;

            dNeta_dmeson_global[idx].fill(eta);
            if (pT > 5.0)
              dNeta_dmeson_pt5[idx].fill(eta);
            if (pT > 10.0)
              dNeta_dmeson_pt10[idx].fill(eta);
          }
        }
      }
    }

    // Preenche os histogramas de multiplicidade ao final de cada evento
    for (int idx = 0; idx < 9; ++idx)
    {
      mult_charm_global[idx].fill(n_charm_glob[idx]);
      mult_charm_pt5[idx].fill(n_charm_pt5[idx]);
      mult_charm_pt10[idx].fill(n_charm_pt10[idx]);

      mult_parton_global[idx].fill(n_parton_glob[idx]);
      mult_parton_pt5[idx].fill(n_parton_pt5[idx]);
      mult_parton_pt10[idx].fill(n_parton_pt10[idx]);

      mult_dmeson_global[idx].fill(n_dmeson_glob[idx]);
      mult_dmeson_pt5[idx].fill(n_dmeson_pt5[idx]);
      mult_dmeson_pt10[idx].fill(n_dmeson_pt10[idx]);
    }
  }



  // Salvamento estruturado nas pastas de pT
  std::string baseOut = "../../Output/pp/Soft_pp/eCM_" + eCM_str + "GeV/";
  std::string suffixes[9] = {"0", "1", "2", "3", "4", "5", "6", "7", "Asym"};
  std::string ptFolders[3] = {"pt_gt_0GeV", "pt_gt_5GeV", "pt_gt_10GeV"};

  for (int t = 0; t < 3; ++t)
  {
    std::string dirOutput = baseOut + ptFolders[t] + "/";
    fs::create_directories(dirOutput);

    for (int i = 0; i < 9; ++i)
    {
      std::string suf = suffixes[i];

      if (t == 0)
      {
        // Multiplicidade (mantém o nome original que você usava)
        mult_charm_global[i].table(dirOutput + "histcharmTotal" + suf + ".dat");
        mult_parton_global[i].table(dirOutput + "histcFinalPartonLevel" + suf + ".dat");
        mult_dmeson_global[i].table(dirOutput + "histDmeson" + suf + ".dat");

        // dN/deta (com prefixo diferenciado para a análise diferencial)
        dNeta_charm_global[i].table(dirOutput + "dNeta_charmTotal" + suf + ".dat");
        dNeta_parton_global[i].table(dirOutput + "dNeta_cFinalPartonLevel" + suf + ".dat");
        dNeta_dmeson_global[i].table(dirOutput + "dNeta_Dmeson" + suf + ".dat");
      }
      else if (t == 1)
      {
        mult_charm_pt5[i].table(dirOutput + "histcharmTotal" + suf + ".dat");
        mult_parton_pt5[i].table(dirOutput + "histcFinalPartonLevel" + suf + ".dat");
        mult_dmeson_pt5[i].table(dirOutput + "histDmeson" + suf + ".dat");

        dNeta_charm_pt5[i].table(dirOutput + "dNeta_charmTotal" + suf + ".dat");
        dNeta_parton_pt5[i].table(dirOutput + "dNeta_cFinalPartonLevel" + suf + ".dat");
        dNeta_dmeson_pt5[i].table(dirOutput + "dNeta_Dmeson" + suf + ".dat");
      }
      else
      {
        mult_charm_pt10[i].table(dirOutput + "histcharmTotal" + suf + ".dat");
        mult_parton_pt10[i].table(dirOutput + "histcFinalPartonLevel" + suf + ".dat");
        mult_dmeson_pt10[i].table(dirOutput + "histDmeson" + suf + ".dat");

        dNeta_charm_pt10[i].table(dirOutput + "dNeta_charmTotal" + suf + ".dat");
        dNeta_parton_pt10[i].table(dirOutput + "dNeta_cFinalPartonLevel" + suf + ".dat");
        dNeta_dmeson_pt10[i].table(dirOutput + "dNeta_Dmeson" + suf + ".dat");
      }
    }
  }

  cout << "Simulação finalizada e arquivos salvos com sucesso e salvos em" + baseOut + "!" << endl;

  return 0;
}