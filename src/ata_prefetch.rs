// [CBT_DAO | VITA Project v1.1]
// 功能：高性能代币账户预创建逻辑 (ATA Prefetch)
// 目标：减少高频交易中的账户初始化延迟，锁定 1,000,000 USDT 路径

use solana_client::rpc_client::RpcClient;
use solana_sdk::{
    instruction::Instruction,
    pubkey::Pubkey,
    signature::{Keypair, Signer},
    transaction::Transaction,
    commitment_config::CommitmentConfig,
};
use spl_associated_token_account::{
    get_associated_token_address,
    instruction::create_associated_token_account,
};
use std::error::Error;

pub struct VitaAtaManager {
    rpc_client: RpcClient,
}

impl VitaAtaManager {
    pub fn new(rpc_url: &str) -> Self {
        Self {
            rpc_client: RpcClient::new_with_commitment(rpc_url.to_string(), CommitmentConfig::confirmed()),
        }
    }

    /// 真实执行逻辑：预检并创建关联代币账户 (ATA)
    pub fn prefetch_ata(
        &self,
        payer: &Keypair,
        token_mint: &Pubkey,
    ) -> Result<String, Box<dyn Error>> {
        let wallet_pubkey = payer.pubkey();
        let ata_address = get_associated_token_address(&wallet_pubkey, token_mint);

        // 风险对冲逻辑：检查账户是否存在，避免重复支付租金 (Rent)
        if self.rpc_client.get_account(&ata_address).is_err() {
            println!("[VITA] 检测到新资产路径，正在预热 ATA: {:?}", ata_address);

            let instruction = create_associated_token_account(
                &wallet_pubkey, // 付款人 (CBT_DAO 地址)
                &wallet_pubkey, // 钱包所有者
                token_mint,     // 代币 Mint 地址
                &spl_token::id(),
            );

            // 物理路径确认：获取最新区块哈希并构建交易
            let recent_blockhash = self.rpc_client.get_latest_blockhash()?;
            let transaction = Transaction::new_signed_with_payer(
                &[instruction],
                Some(&wallet_pubkey),
                &[payer],
                recent_blockhash,
            );

            // 真实发送并确认交易
            let signature = self.rpc_client.send_and_confirm_transaction(&transaction)?;
            Ok(format!("成功锁定账户，交易哈希: {}", signature))
        } else {
            Ok(format!("账户已存在，无需额外燃料损耗。"))
        }
    }
}

// 示例调用逻辑 (供开发者参考)
// let manager = VitaAtaManager::new("https://api.mainnet-beta.solana.com");
// manager.prefetch_ata(&my_keypair, &mint_pubkey);
