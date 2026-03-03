// Solana Anchor Framework 模拟逻辑 (2026 简化版)
use anchor_lang::prelude::*;

declare_id!("ClaimGuard11111111111111111111111111111");

#[program]
pub mod asset_recovery_vault {
    use super::*;

    // 1. 初始化回收任务：锁定发现的资产信息
    pub fn initialize_report(ctx: Context<InitReport>, val: u64) -> Result<()> {
        let report = &mut ctx.accounts.report;
        report.total_value = val;
        report.commission = val * 20 / 100; // 自动计算 20% 佣金
        report.is_paid = false;
        Ok(())
    }

    // 2. 用户支付佣金，解锁“领取路径”或“私钥分片”
    pub fn unlock_path(ctx: Context<Unlock>) -> Result<()> {
        let report = &mut ctx.accounts.report;
        // 物理路径：用户向你的钱包转账 commission 数量的 SOL/USDT
        // 逻辑对冲：支付成功后，触发前端显示 Claim Link
        report.is_paid = true;
        Ok(())
    }
}

#[account]
pub struct RecoveryReport {
    pub total_value: u64,
    pub commission: u64,
    pub is_paid: bool,
}
