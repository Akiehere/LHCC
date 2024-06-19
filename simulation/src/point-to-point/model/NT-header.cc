/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2009 New York University
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Author: Adrian S.-W. Tam <adrian.sw.tam@gmail.com>
 */

#include <stdint.h>
#include <iostream>
#include "ns3/buffer.h"
#include "ns3/address-utils.h"
#include "ns3/log.h"
#include "NT-header.h"

NS_LOG_COMPONENT_DEFINE ("RttHeader");

namespace ns3 {

NS_OBJECT_ENSURE_REGISTERED (NTHeader);

NTHeader::NTHeader ()
{ 
  dport=0;
  rate=0;
  ih={0};
}


NTHeader::~NTHeader ()
{}

TypeId
NTHeader::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::RttHeader")
    .SetParent<Header> ()
    .AddConstructor<NTHeader> ()
    ;
  return tid;
}

TypeId
NTHeader::GetInstanceTypeId (void) const
{
  return GetTypeId ();
}

void NTHeader::Print (std::ostream &os) const
{
  return;
}
uint32_t NTHeader::GetSerializedSize (void)  const
{
  return sizeof(rate)+sizeof(ih)+sizeof(dport);
}
void NTHeader::Serialize (Buffer::Iterator start)  const
{ 
  start.WriteU16(dport);
  start.WriteU16 (rate);
  start.WriteU32(ih.buf[0]);
	start.WriteU32(ih.buf[1]);
}

uint32_t NTHeader::Deserialize (Buffer::Iterator start)
{
  dport=start.ReadLsbtohU16();
  rate = start.ReadU16 ();
  ih.buf[0]=start.ReadU32();
  ih.buf[1]=start.ReadU32();
  return GetSerializedSize ();
}


}; // namespace ns3
